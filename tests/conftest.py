# Python
import os

# LogMeIn API
import lmiapi

# Py.Test
import pytest


@pytest.fixture(scope='session')
def central_email():
    email = os.environ.get('LMIAPI_EMAIL', '')
    if not email:
        pytest.skip('LMIAPI_EMAIL environment variable must be defined to test central "API"')
    return email


@pytest.fixture(scope='session')
def central_password():
    password = os.environ.get('LMIAPI_PASSWORD', '')
    if not password:
        pytest.skip('LMIAPI_PASSWORD environment variable must be defined to test central "API"')
    return password


@pytest.fixture()
def central_api(central_email, central_password):
    return lmiapi.LogMeInCentralAPI(email=central_email, password=central_password)


@pytest.fixture(scope='session')
def api_company_id():
    company_id = int(os.environ.get('LMIAPI_COMPANY_ID', '') or 0)
    if not company_id:
        pytest.skip('LMIAPI_COMPANY_ID environment variable must be defined to test public API')
    return company_id


@pytest.fixture(scope='session')
def api_psk():
    psk = os.environ.get('LMIAPI_PSK', '')
    if not psk:
        pytest.skip('LMIAPI_PSK environment variable must be defined to test public API')
    return psk


@pytest.fixture(scope='session')
def api_auth_file():
    auth_file = os.environ.get('LMIAPI_AUTH_FILE', '')
    if not auth_file:
        pytest.skip('LMIAPI_AUTH_FILE environment variable must be defined to test public API')
    return auth_file


@pytest.fixture(scope='session')
def api_auth_file_content(api_auth_file):
    return file(api_auth_file).read()


@pytest.fixture(scope='session')
def public_api_v1_class():
    return lmiapi.LogMeInPublicAPIv1


@pytest.fixture()
def public_api_v1(public_api_v1_class, api_company_id, api_psk):
    return public_api_v1_class(dict(companyId=api_company_id, psk=api_psk))


@pytest.fixture()
def public_api_v1_auth_file(public_api_v1_class, api_auth_file):
    return public_api_v1_class(api_auth_file)


@pytest.fixture()
def public_api_v1_auth_file_content(public_api_v1_class, api_auth_file_content):
    return public_api_v1_class(api_auth_file_content)


@pytest.fixture(scope='session')
def public_api_v2_class():
    return lmiapi.LogMeInPublicAPIv2


@pytest.fixture()
def public_api_v2(public_api_v2_class, api_company_id, api_psk):
    return public_api_v2_class(dict(companyId=api_company_id, psk=api_psk))


@pytest.fixture()
def public_api_v2_auth_file(public_api_v2_class, api_auth_file):
    return public_api_v2_class(api_auth_file)


@pytest.fixture()
def public_api_v2_auth_file_content(public_api_v2_class, api_auth_file_content):
    return public_api_v2_class(api_auth_file_content)
