# Python
import logging
import warnings

# LogMeIn API
from .public import LogMeInPublicAPIBase

__all__ = ['LogMeInPublicAPIv2', 'LogMeInPublicAPI', 'LogMeInAPI']

logger = logging.getLogger('lmiapi.public_v2')


class LogMeInPublicAPIv2(LogMeInPublicAPIBase):
    '''
    https://developer.logmein.com/api/api-reference/
    '''

    API_ROOT = 'https://secure.logmein.com/public-api/v2/'

    def __init__(self, creds):
        super(LogMeInPublicAPIv2, self).__init__(creds)
        self.session.headers.update({'Accept': 'application/json; charset=utf-8'})

    def authentication(self):
        # v2 authentication still uses v1 authentication URL.
        return self._get('/authentication', v1=True)

    def list_hosts(self):
        return self._get('/hosts')

    def list_hosts_with_groups(self):
        return self._get('/hostswithgroups')

    def change_host_description(self, host_id, new_description):
        path = '/hosts/{}/description'.format(host_id)
        data = {
            'newDescription': new_description,
        }
        return self._put(path, data, v1=True)

    def move_hosts_to_group(self, group_id, *host_ids):
        path = '/host-groups/{}/hosts'.format(group_id)
        data = {
            'hostIds': list(map(int, host_ids)),
        }
        return self._put(path, data, v1=True)

    def connect_to_host(self, host_id, direct_link=True, fail_when_session=False):
        path = '/hosts/{}/connection'.format(host_id)
        data = {
            'directLink': direct_link,
            'failWhenRaSessionInProgress': fail_when_session,
        }
        return self._post(path, data, v1=True)

    def delete_hosts(self, *host_ids):
        path = '/hosts'
        data = {
            'hostIds': list(map(int, host_ids)),
        }
        return self._delete(path, data, v1=True)

    def get_hardware_inventory_fields(self):
        return self._get('/inventory/hardware/fields', v1=True)

    def create_hardware_inventory_report(self, host_ids, fields=None):
        if not isinstance(host_ids, (list, tuple, set, frozenset)):
            host_ids = [host_ids]
        data = {
            'hostIds': list(map(int(host_ids))),
        }
        if fields:
            data['fields'] = list(map(str(fields)))
        return self._post('/inventory/hardware/reports', data, v1=True)

    def get_hardware_inventory_reports(self):
        return self._get('/inventory/hardware/reports', v1=True)

    def get_hardware_inventory_report(self, report_id):
        path = '/inventory/hardware/reports/{}'.format(report_id)
        return self._get(path, v1=True)

    def get_system_inventory_fields(self):
        return self._get('/inventory/system/fields', v1=True)

    def create_system_inventory_report(self, host_ids, fields=None):
        if not isinstance(host_ids, (list, tuple, set, frozenset)):
            host_ids = [host_ids]
        data = {
            'hostIds': list(map(int(host_ids))),
        }
        if fields:
            data['fields'] = list(map(str(fields)))
        return self._post('/inventory/system/reports', data, v1=True)

    def get_system_inventory_reports(self):
        return self._get('/inventory/system/reports', v1=True)

    def get_system_inventory_report(self, report_id):
        path = '/inventory/system/reports/{}'.format(report_id)
        return self._get(path, v1=True)

    def get_custom_field_categories(self):
        return self._get('/hosts/custom-fields/categories', v1=True)

    def get_custom_field_values(self):
        return self._get('/hosts/custom-fields', v1=True)

    def get_anti_virus_details(self):
        return self._get('/hosts/anti-virus/details', v1=True)

    def refresh_anti_virus_status(self, *host_ids):
        data = {
            'targetHostIds': list(map(int(host_ids))),
        }
        return self._post('/anti-virus/actions/refresh-status', data, v1=True)

    def start_anti_virus_full_scan(self, *host_ids):
        data = {
            'targetHostIds': list(map(int(host_ids))),
        }
        return self._post('/anti-virus/actions/start-fullscan', data, v1=True)

    def enable_anti_virus_real_time_protection(self, *host_ids):
        data = {
            'targetHostIds': list(map(int(host_ids))),
        }
        return self._post('/anti-virus/actions/enable-realtimeprotection', data, v1=True)

    def update_anti_virus_definitions(self, *host_ids):
        data = {
            'targetHostIds': list(map(int(host_ids))),
        }
        return self._post('/anti-virus/actions/update-definition', data, v1=True)

    def install_kapersky_endpoint_security(self, *host_ids):
        data = {
            'targetHostIds': list(map(int(host_ids))),
        }
        return self._post('/anti-virus/actions/install-kaspersky-endpoint-security', data, v1=True)


class LogMeInAPI(LogMeInPublicAPIv2):

    def __init__(self, *args, **kwargs):
        warnings.warn('The LogMeInAPI class is deprecated; use '
                      'LogMeInPublicAPIv2 instead.', DeprecationWarning)
        super(LogMeInAPI, self).__init__(*args, **kwargs)


class LogMeInPublicAPI(LogMeInPublicAPIv2):

    def __init__(self, *args, **kwargs):
        warnings.warn('The LogMeInPublicAPI class is deprecated; use '
                      'LogMeInPublicAPIv2 instead.', DeprecationWarning)
        super(LogMeInPublicAPI, self).__init__(*args, **kwargs)
