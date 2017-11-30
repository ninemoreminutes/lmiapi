#!/usr/bin/env python

# Python
import logging
import os
import pprint

# LogMeIn API
from lmiapi import LogMeInCentralAPI

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(name)s:%(message)s')

# Read authentication settings from environment variables.
email = os.environ.get('LMIAPI_EMAIL', 'logmein@example.com')
password = os.environ.get('LMIAPI_PASSWORD', 'l0gm31n')

api = LogMeInCentralAPI(email=email, password=password)
profiles = api.get_user_profile_list()
pprint.pprint(profiles, indent=4)
print
# for profile_id, name in profiles.items():
#     print api.select_profile(profile_id)
#     hosts = api.get_all_hosts()
#     pprint.pprint(hosts, indent=4)
#     print

profile_id = [x[0] for x in profiles.items() if 'res' in x[1].lower()][0]
print api.select_profile(profile_id)

hosts = api.get_all_hosts()
# pprint.pprint(hosts, indent=4)

host_list = hosts['GetAllHostsForCentralResult']['Hosts']
print

for host_info in host_list:
    host_details = api.get_host_details(host_info['hostid'])
    host_details.update(host_info)
    pprint.pprint(host_details, indent=4)
    host_av_info = api.get_host_av_info(host_info['hostid'])
    pprint.pprint(host_av_info, indent=4)
    print
    if host_details['status'] in (1, 4):
        # api.connect_to_host(host_info['hostid'])
        break
# pprint.pprint(host_info, indent=4)
