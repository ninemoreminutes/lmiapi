# Python
import json
import logging
import os
import re
import urllib
import urlparse
import webbrowser

# Requests
import requests

# BeautifulSoup4
from bs4 import BeautifulSoup

__all__ = ['LogMeInCentralAPI']

logger = logging.getLogger('lmiapi.central')


class LogMeInCentralAPI(object):

    API_ROOT = 'https://secure.logmein.com/api/'

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/JSON'})
        self.current_profile_id = None

    def _post(self, path, data=None):
        url = '%s%s' % (self.API_ROOT, path.lstrip('/'))
        headers = {'Content-Type': 'application/JSON'}
        data = json.dumps(data or {})
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 401 and self.login():
            response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()
        #logger.debug('POST %s -> %d', url, response.status_code)
        return response.json()

    def _update_current_profile_id(self, soup):
        profile_id = None
        alt_link = soup.find('link', rel='alternate', href=re.compile(r'^.*?profileid=\d+?.*?$'))
        if alt_link:
            alt_parts = urlparse.urlsplit(alt_link['href'])
            alt_query = urlparse.parse_qs(alt_parts.query)
            profile_id = int(alt_query.get('profileid', ['0'])[0])
        self.current_profile_id = profile_id or None
        logger.debug('current profile id: %s', str(self.current_profile_id))
        return self.current_profile_id

    def login(self):
        # Read main LogMeIn page at secure.logmein.com.
        url = urlparse.urljoin(self.API_ROOT, '/')
        response = self.session.get(url)
        response.raise_for_status()
        # Find login button link.
        soup = BeautifulSoup(response.text)
        btn_login = soup.find('a', attrs={'class': 'btn-login', 'href': True})
        if not btn_login:
            raise RuntimeError('Unable to find login button link!')
        login_url = urlparse.urljoin(response.url, btn_login['href'])
        # Follow the login link.
        response = self.session.get(login_url)
        response.raise_for_status()
        # Try to find the current profile ID in the response.  If found, we're
        # already logged in.
        soup = BeautifulSoup(response.text)
        profile_id = self._update_current_profile_id(soup)
        if profile_id:
            return profile_id
        # Otherwise, we were redirected to the login page, so find the login
        # form and build up the auth data to send.
        form = soup.find('form', id='form', action=True)
        if not form:
            raise RuntimeError('No login form could be found!')
        auth_url = urlparse.urljoin(response.url, form['action'])
        auth_method = form.attrs.get('method', 'POST').lower()
        fields = form.find_all('input', attrs={'name': True})
        auth_data = {}
        for field in fields:
            name = field['name']
            if name == 'email':
                value = self.email
            elif name == 'password':
                value = self.password
            else:
                value = field.attrs.get('value', '')
            auth_data[name] = value
        # Now submit the login form with the auth data filled in.
        logger.debug('auth url: %s %s', auth_method.upper(), auth_url)
        logger.debug('auth data: %r', auth_data)
        response = getattr(self.session, auth_method)(auth_url, auth_data)
        response.raise_for_status()
        # Look for the current profile ID in the response.
        soup = BeautifulSoup(response.text)
        return self._update_current_profile_id(soup)

    def select_profile(self, profile_id):
        # Get the URL used to switch to a new profile.
        url = urlparse.urljoin(self.API_ROOT, '/login/selectprofile.aspx?profile=%d' % profile_id)
        response = self.session.get(url)
        response.raise_for_status()
        # Look for the new profile ID in the response.
        soup = BeautifulSoup(response.text)
        return self._update_current_profile_id(soup)

    def get_user_profile_list(self):
        result = self._post('ProfileList.svc/GetUserProfileList')
        return dict([(x['Id'], x['Name']) for x in result['GetUserProfileListResult']['List']])

    def get_all_hosts(self):
        result = self._post('Computers.svc/GetAllHostsForCentral')
        return result

    def get_host_details(self, host_id):
        url = urlparse.urljoin(self.API_ROOT, '/mycomputers_preferences.asp')
        response = self.session.get(url, params={'hostid': host_id})
        response.raise_for_status()
        soup = BeautifulSoup(response.text)
        host_details = {}
        for hostid_input in soup.select('fieldset > input[name="hostid"]'):
            host_details[u'hostid'] = int(hostid_input['value'])
        for profileid_input in soup.select('fieldset input[name="profileid"]'):
            host_details[u'profileid'] = int(profileid_input['value'])
        for tr in soup.select('fieldset table tr'):
            for n, td in enumerate(tr.find_all('td', recursive=False)):
                if n == 0:
                    key_parts = td.get_text(strip=True).replace(':', '').split()
                    key_parts = [x.strip().title() for x in key_parts]
                    key_parts[0] = key_parts[0].lower()
                    key = u''.join(key_parts)
                    if key == 'status':
                        key = u'statusString'
                    elif key == 'group':
                        key = u'groupName'
                elif n == 1:
                    if key == 'computerDescription':
                        value = td.find('input', attrs={'name': 'desc'})['value']
                    elif key == 'statusString':
                        value = td.get_text('|', strip=True).split('|')[0]
                        a_tag = td.find('a', href=True)
                        if a_tag:
                            host_details[u'connectUrl'] = urlparse.urljoin(response.url, a_tag['href'])
                    elif key == 'groupName':
                        selected_option = td.find('option', selected=True)
                        value = selected_option.get_text()
                        host_details[u'groupid'] = int(selected_option['value'])
                    elif key == 'note':
                        value = td.find('textarea').get_text()
                    else:
                        value = td.get_text(strip=True)
                    host_details[key] = value
        return host_details

    def get_host_av_info(self, host_id):
        result = self._post('AntiVirus.svc/GetHostAVInfo', {'hostId': host_id})
        return result['GetHostAVInfoResult']

    def connect_to_host(self, host_id):
        url = urlparse.urljoin(self.API_ROOT, '/mycomputers_connect.asp')
        qs = urllib.urlencode({'hostid': host_id})
        url = '%s?%s' % (url, qs)
        webbrowser.open_new_tab(url)
        return
        response = self.session.get(url, params={'hostid': host_id})
        response.raise_for_status()
        soup = BeautifulSoup(response.text)
        meta = soup.find('meta', attrs={'http-equiv': 'refresh', 'content': True})
        url = meta['content'].split(';URL=', 1)[1]
        response = self.session.get(url)
