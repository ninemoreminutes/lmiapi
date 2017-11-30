# Py.test
import pytest

pytestmark = pytest.mark.nondestructive


def test_auth_with_company_id_and_psk(public_api_v1):
    result = public_api_v1.authentication()
    assert result and result.get('success')


def test_auth_with_auth_file(public_api_v1_auth_file):
    result = public_api_v1_auth_file.authentication()
    assert result and result.get('success')


def test_auth_with_auth_file_content(public_api_v1_auth_file_content):
    result = public_api_v1_auth_file_content.authentication()
    assert result and result.get('success')


def test_hosts(public_api_v1):
    public_api_v1.hosts()


def test_hardware_fields(public_api_v1):
    public_api_v1.hardware_fields()


def test_system_fields(public_api_v1):
    public_api_v1.system_fields()


@pytest.mark.xfail
def test_hardware_report(public_api_v1):
    public_api_v1.hardware_report()


@pytest.mark.xfail
def test_system_report(public_api_v1):
    public_api_v1.system_report()
