# Python
import logging
import warnings

# LogMeIn API
from .public import LogMeInPublicAPIBase

__all__ = ['LogMeInPublicAPIv1']

logger = logging.getLogger('lmiapi.public_v1')


class LogMeInPublicAPIv1(LogMeInPublicAPIBase):
    '''
    https://secure.logmein.com/welcome/documentation/EN/pdf/LogMeInCentralPublicAPIReference.pdf
    '''

    API_ROOT = 'https://secure.logmein.com/public-api/v1/'

    def __init__(self, creds):
        warnings.warn('The LogMeInPublicAPIv1 class is no longer the current '
                      'version; use LogMeInPublicAPIv2 instead.',
                      DeprecationWarning)
        super(LogMeInPublicAPIv1, self).__init__(creds)

    def hosts(self):
        d = self._get('/hosts')
        if 'hosts' in d:
            self._cached_hosts = d
        return getattr(self, '_cached_hosts', d)

    def _get_or_create_report(self, path, host_ids=None, fields=None):  # pragma: no cover
        d = self._get(path)
        if not d or not d.get('token', None) or not d.get('expires', None):
            if host_ids is None:
                host_ids = [x['id'] for x in self.hosts().get('hosts', {})]
            elif callable(host_ids):
                host_ids = host_ids()
            if fields is None:
                fields = []
            elif callable(fields):
                fields = fields()
            post_data = {
                'hostIds': host_ids,
                'fields': fields
            }
            d = self._post(path, post_data)
        token = d.get('token', None)
        result = {'report': dict(d.items()), 'hosts': {}}
        while token:
            d = self._get('%s/%s' % (path, token))
            result['hosts'].update(d['hosts'])
            token = d['report']['token']
        return result

    def hardware_fields(self):
        return self._get('/inventory/hardware/fields')

    def hardware_report(self, host_ids=None, fields=None):
        if fields is None:
            fields = self.hardware_fields
        return self._get_or_create_report('/inventory/hardware/reports',
                                          host_ids, fields)

    def system_fields(self):
        return self._get('/inventory/system/fields')

    def system_report(self, host_ids=None, fields=None):
        if fields is None:
            fields = self.system_fields
        return self._get_or_create_report('/inventory/system/reports',
                                          host_ids, fields)
