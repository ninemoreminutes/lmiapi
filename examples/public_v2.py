#!/usr/bin/env python

# Python
import logging
import os

# LogMeIn API
from lmiapi import LogMeInPublicAPIv2

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(name)s:%(message)s')

# Read authentication settings from environment variables.
company_id = int(os.environ.get('LMIAPI_COMPANY_ID', '1234567890'))
psk = os.environ.get('LMIAPI_PSK', 'abcde12345ABCDE12345')
auth_file = os.environ.get('LMIAPI_AUTH_FILE', 'public_auth.txt')

# Option 1: Pass credentials as a dictionary.
auth = {'companyId': company_id, 'psk': psk}
api = LogMeInPublicAPIv2(auth)

# Option 2: Pass the content of the credentials file provided by LogMeIn.
auth = file(auth_file).read()
api = LogMeInPublicAPIv2(auth)

# Option 3: Pass in the credentials file name directly.
api = LogMeInPublicAPIv2(auth_file)

# Check that credentials work to authenticate.
print api.authentication()

# Get host ID/description for all hosts.
print api.list_hosts()

# Get host ID/description/group for all hosts.
print api.list_hosts_with_groups()

# Get list of hardware report fields.
print api.get_hardware_inventory_fields()

# Get list of system report fields.
print api.get_system_inventory_fields()
