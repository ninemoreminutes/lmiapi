# Py.test
import pytest

pytestmark = pytest.mark.nondestructive


def test_login(central_api):
    central_api.login()


def test_get_user_profile_list(central_api):
    profiles = central_api.get_user_profile_list()
    assert profiles


def test_select_profile(central_api):
    profiles = central_api.get_user_profile_list()
    profile_id = [x[0] for x in profiles.items() if 'res' in x[1].lower()][0]
    central_api.select_profile(profile_id)


def test_get_all_hosts(central_api):
    hosts = central_api.get_all_hosts()
    host_list = hosts['GetAllHostsForCentralResult']['Hosts']

    for host_info in host_list:
        host_details = central_api.get_host_details(host_info['hostid'])
        host_details.update(host_info)
        host_av_info = central_api.get_host_av_info(host_info['hostid'])
        assert host_av_info
        if host_details['status'] in (1, 4):
            # central_api.connect_to_host(host_info['hostid'])
            break
