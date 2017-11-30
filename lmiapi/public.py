# Python
import json
import logging
import os

# Requests
import requests
from requests.structures import CaseInsensitiveDict

__all__ = []

logger = logging.getLogger('lmiapi.public')


class LogMeInPublicAPIBase(object):

    API_ROOT = None

    def __init__(self, creds):
        assert self.API_ROOT
        self.creds = self._check_creds(creds)
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/JSON'})
        self.session.headers.update({'Authorization': json.dumps(self.creds)})

    def _check_creds(self, creds):
        d = CaseInsensitiveDict()
        if isinstance(creds, dict):
            d.update(creds)
        elif isinstance(creds, basestring):
            if os.path.exists(creds):
                creds = file(creds, 'r').read()
            for line in creds.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    d[k.strip()] = v.strip()
        else:
            raise TypeError('unsupported type for credentials data')
        if 'companyId' not in d and 'CID' in d:
            d['companyId'] = d['CID']
        if 'companyId' in d and 'psk' not in d:
            raise ValueError('psk is required when companyId is provided')
        elif 'psk' in d and 'companyId' not in d:
            raise ValueError('companyId is required when psk is provided')
        elif 'companyId' in d and 'psk' in d:
            return {
                'companyId': int(d['companyId']),
                'psk': str(d['psk']),
            }
        elif 'loginSessionId' in d and 'profileId' not in d:
            raise ValueError('profileId is required when loginSessionId is '
                             'provided')
        elif 'profileId' in d and 'loginSessionId' not in d:
            raise ValueError('loginSessionId is required when profileId is '
                             'provided')
        elif 'loginSessionId' in d and 'profileId' in d:
            return {
                'loginSessionId': str(d['loginSessionId']),
                'profileId': int(d['profileId']),
            }
        else:
            raise ValueError('either companyId+psk or '
                             'loginSessionId+profileId must be provided')

    def _get(self, path, v1=False):
        api_root = self.API_ROOT.replace('/v2/', '/v1/') if v1 else self.API_ROOT
        url = '{}{}'.format(api_root, path.lstrip('/'))
        response = self.session.get(url)
        logger.debug('GET %s -> %d', url, response.status_code)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()

    def _post(self, path, data=None, v1=False):
        api_root = self.API_ROOT.replace('/v2/', '/v1/') if v1 else self.API_ROOT
        url = '{}{}'.format(api_root, path.lstrip('/'))
        if data:
            headers = {'Content-Type': 'application/JSON'}
            data = json.dumps(data)
        else:
            headers = {}
            data = None
        response = self.session.post(url, data=data, headers=headers)
        logger.debug('POST %s -> %d', url, response.status_code)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()

    def _put(self, path, data, v1=False):
        api_root = self.API_ROOT.replace('/v2/', '/v1/') if v1 else self.API_ROOT
        url = '{}{}'.format(api_root, path.lstrip('/'))
        headers = {'Content-Type': 'application/JSON'}
        data = json.dumps(data)
        response = self.session.put(url, data=data, headers=headers)
        logger.debug('PUT %s -> %d', url, response.status_code)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()

    def _delete(self, path, data=None, v1=False):
        api_root = self.API_ROOT.replace('/v2/', '/v1/') if v1 else self.API_ROOT
        url = '{}{}'.format(api_root, path.lstrip('/'))
        if data:
            headers = {'Content-Type': 'application/JSON'}
            data = json.dumps(data)
        else:
            headers = {}
            data = None
        response = self.session.delete(url, data=data, headers=headers)
        logger.debug('DELETE %s -> %d', url, response.status_code)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()

    def authentication(self):
        return self._get('/authentication')
