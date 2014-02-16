#!/usr/bin/env python

# Python
import logging

# LogMeIn API
from lmiapi import LogMeInAPI

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(name)s:%(message)s')

# Option 1: Pass credentials as a dictionary.
auth = {'companyId': 123467890, 'psk': 'abcde12345ABCDE12345'}
api = LogMeInAPI(auth)

# Option 2: Pass the content of the credentials file provided by LogMeIn.
auth = file('example_auth.txt').read()
api = LogMeInAPI(auth)

# Option 3: Pass in the credentials file name directly.
api = LogMeInAPI('example_auth.txt')

# Check that credentials work to authenticate.
print api.authentication()

# Get host ID/description for all hosts.
print api.hosts()

# Get list of hardware report fields.
print api.hardware_fields()

# Get list of system report fields.
print api.system_fields()

# Get or create a hardware report (default to all fields, all hosts).
print api.hardware_report()

# Get or create a system report (default to all fields, all hosts).
print api.system_report()
