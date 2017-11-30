# Py.test
import pytest

# pytestmark = pytest.mark.nondestructive


def test_invalid_creds(public_api_v2_class):
    with pytest.raises(TypeError):
        public_api_v2_class(False)
    with pytest.raises(ValueError):
        public_api_v2_class(dict())


def test_auth_with_company_id_and_psk(public_api_v2):
    result = public_api_v2.authentication()
    assert result and result.get('success')


def test_auth_with_auth_file(public_api_v2_auth_file):
    result = public_api_v2_auth_file.authentication()
    assert result and result.get('success')


def test_auth_with_auth_file_content(public_api_v2_auth_file_content):
    result = public_api_v2_auth_file_content.authentication()
    assert result and result.get('success')


def test_list_hosts(public_api_v2):
    result = public_api_v2.list_hosts()
    assert 'hosts' in result and 'groups' not in result
    for host in result['hosts']:
        assert host.get('id')
        assert 'description' in host
        assert 'isHostOnline' in host


def test_list_hosts_with_groups(public_api_v2):
    result = public_api_v2.list_hosts_with_groups()
    assert 'hosts' in result and 'groups' in result
    for group in result['groups']:
        assert group.get('id')
        assert 'name' in group
    for host in result['hosts']:
        assert host.get('id')
        assert 'description' in host
        assert 'isHostOnline' in host
        assert 'groupId' in host


def test_change_host_description(public_api_v2):
    result = public_api_v2.list_hosts()
    host_id = None
    for host in result.get('hosts'):
        host_description = host.get('description', '')
        if 'lmiapi' in host_description.lower():
            host_id = host.get('id', None)
            break
    if not host_id:
        pytest.skip('no host found containing "lmiapi" in the description')
    lmiapi_index = host_description.lower().index('lmiapi')
    lmiapi_text = host_description[lmiapi_index:(lmiapi_index + 6)]
    new_description = host_description.replace(lmiapi_text, lmiapi_text.swapcase())
    public_api_v2.change_host_description(host_id, new_description)


@pytest.mark.skip(reason='test not fully implemented')
def test_move_hosts_to_group(public_api_v2):
    result = public_api_v2.list_hosts_with_groups()
    group_id = None
    for group in result.get('groups'):
        group_description = group.get('description', '')
        if 'lmiapi' in group_description.lower():
            group_id = group.get('id', None)
            break
    if not group_id:
        pytest.skip('no group found containing "lmiapi" in the description')


@pytest.mark.skip(reason='test not fully implemented')
def test_connect_to_host(public_api_v2):
    result = public_api_v2.list_hosts()
    host_id = None
    for host in result.get('hosts'):
        if not host.get('isHostOnline', False):
            continue
        host_description = host.get('description', '')
        if 'lmiapi' in host_description.lower():
            host_id = host.get('id', None)
            break
    if not host_id:
        pytest.skip('no host found containing "lmiapi" in the description')
    result = public_api_v2.connect_to_host(host_id)


@pytest.mark.skip(reason='test not fully implemented')
def test_delete_host(public_api_v2):
    result = public_api_v2.list_hosts()
    host_id = None
    for host in result.get('hosts'):
        host_description = host.get('description', '')
        if 'lmiapi-delete' in host_description.lower():
            host_id = host.get('id', None)
            break
    if not host_id:
        pytest.skip('no host found containing "lmiapi-delete" in the description')
    result = public_api_v2.delete_hosts(host_id)


def test_get_hardware_inventory_fields(public_api_v2):
    fields = public_api_v2.get_hardware_inventory_fields()
    assert fields


@pytest.mark.skip(reason='test not fully implemented')
def test_hardware_inventory_reports(public_api_v2):
    fields = public_api_v2.get_hardware_inventory_fields()
    assert fields
    result = public_api_v2.get_hardware_inventory_reports()
    if not result.get('token') or not result.get('expires'):
        hosts = public_api_v2.list_hosts()
        host_ids = [host.get('id') for host in hosts.get('hosts')][:50]
        result = public_api_v2.create_hardware_inventory_report(*host_ids, fields=fields)
        assert result.get('token')
        assert result.get('expires')
    result = public_api_v2.get_hardware_inventory_reports()
    assert result.get('token')
    assert result.get('expires')
    result = public_api_v2.get_hardware_inventory_report(result['token'])
    assert result.get('report')
    assert result.get('hosts')


def test_get_system_inventory_fields(public_api_v2):
    fields = public_api_v2.get_system_inventory_fields()
    assert fields


@pytest.mark.skip(reason='test not fully implemented')
def test_system_inventory_reports(public_api_v2):
    fields = public_api_v2.get_system_inventory_fields()
    assert fields
    result = public_api_v2.get_system_inventory_reports()
    if not result.get('token') or not result.get('expires'):
        hosts = public_api_v2.list_hosts()
        host_ids = [host.get('id') for host in hosts.get('hosts')][:50]
        result = public_api_v2.create_system_inventory_report(*host_ids, fields=fields)
        assert result.get('token')
        assert result.get('expires')
    result = public_api_v2.get_system_inventory_reports()
    assert result.get('token')
    assert result.get('expires')
    result = public_api_v2.get_system_inventory_report(result['token'])
    assert result.get('report')
    assert result.get('hosts')


def test_custom_fields(public_api_v2):
    categories = public_api_v2.get_custom_field_categories()
    assert categories
    assert 'metadataCategories' in categories
    category_map = {}
    for metadata_category in categories['metadataCategories']:
        assert metadata_category.get('id')
        assert metadata_category.get('name')
        assert 'values' in metadata_category
        category_map[metadata_category['id']] = {
            'name': metadata_category['name'],
            'values': {},
        }
        for metadata_value in metadata_category['values']:
            assert metadata_value.get('id')
            assert metadata_value.get('name')
            category_map[metadata_category['id']]['values'][metadata_value['id']] = metadata_value['name']
    values = public_api_v2.get_custom_field_values()
    assert values
    assert 'hosts' in values
    for host in values['hosts']:
        assert 'id' in host
        assert 'metadata' in host
        for metadata in host['metadata']:
            assert metadata.get('categoryId')
            assert metadata.get('valueId')
            assert metadata['categoryId'] in category_map
            assert metadata['valueId'] in category_map[metadata['categoryId']]['values']


@pytest.mark.skip(reason='test not fully implemented')
def test_get_anti_virus_details(public_api_v2):
    result = public_api_v2.get_anti_virus_details()
    assert result
    assert 'hostGroups' in result
    assert 'hosts' in result
    for host in result.get('hosts'):
        assert 'hostId' in host
        assert 'antiVirusStatus' in host
