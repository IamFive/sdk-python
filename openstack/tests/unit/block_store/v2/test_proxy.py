# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.block_store.v2 import _proxy
from openstack.block_store.v2 import snapshot
from openstack.block_store.v2 import type
from openstack.block_store.v2 import volume
from openstack.tests.unit import test_proxy_base2
from openstack.tests.unit.test_proxy_base3 import BaseProxyTestCase
from openstack.block_store import block_store_service


class TestVolumeProxy(test_proxy_base2.TestProxyBase):
    def setUp(self):
        super(TestVolumeProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_snapshot_get(self):
        self.verify_get(self.proxy.get_snapshot, snapshot.Snapshot)

    def test_snapshots_detailed(self):
        self.verify_list(self.proxy.snapshots, snapshot.SnapshotDetail,
                         paginated=True,
                         method_kwargs={"details": True, "query": 1},
                         expected_kwargs={"query": 1})

    def test_snapshots_not_detailed(self):
        self.verify_list(self.proxy.snapshots, snapshot.Snapshot,
                         paginated=True,
                         method_kwargs={"details": False, "query": 1},
                         expected_kwargs={"query": 1})

    def test_snapshot_create_attrs(self):
        self.verify_create(self.proxy.create_snapshot, snapshot.Snapshot)

    def test_snapshot_delete(self):
        self.verify_delete(self.proxy.delete_snapshot,
                           snapshot.Snapshot, False)

    def test_snapshot_delete_ignore(self):
        self.verify_delete(self.proxy.delete_snapshot,
                           snapshot.Snapshot, True)

    def test_type_get(self):
        self.verify_get(self.proxy.get_type, type.Type)

    def test_types(self):
        self.verify_list(self.proxy.types, type.Type, paginated=False)

    def test_type_create_attrs(self):
        self.verify_create(self.proxy.create_type, type.Type)

    def test_type_delete(self):
        self.verify_delete(self.proxy.delete_type, type.Type, False)

    def test_type_delete_ignore(self):
        self.verify_delete(self.proxy.delete_type, type.Type, True)

    def test_volume_get(self):
        self.verify_get(self.proxy.get_volume, volume.Volume)

    def test_volumes_detailed(self):
        self.verify_list(self.proxy.volumes, volume.VolumeDetail,
                         paginated=True,
                         method_kwargs={"details": True, "query": 1},
                         expected_kwargs={"query": 1})

    def test_volumes_not_detailed(self):
        self.verify_list(self.proxy.volumes, volume.Volume,
                         paginated=True,
                         method_kwargs={"details": False, "query": 1},
                         expected_kwargs={"query": 1})

    def test_volume_create_attrs(self):
        self.verify_create(self.proxy.create_volume, volume.Volume)

    def test_volume_delete(self):
        self.verify_delete(self.proxy.delete_volume, volume.Volume, False)

    def test_volume_delete_ignore(self):
        self.verify_delete(self.proxy.delete_volume, volume.Volume, True)


class TestVolumeProxy2(BaseProxyTestCase):
    def __init__(self, *args, **kwargs):
        super(TestVolumeProxy2, self).__init__(
            *args,
            proxy_class=_proxy.Proxy,
            service_class=block_store_service.BlockStoreService,
            **kwargs)

    def test_os_quota_set(self):
        self.mock_response_json_file_values('os_quota_set.json')
        quota_set = self.proxy.os_quota_set('tenant-id')
        self.assert_session_get_with('/os-quota-sets/tenant-id?usage=True')

        self.assertIsInstance(quota_set, volume.QuotaSet)
        self.assertEqual(quota_set.gigabytes['in_use'], 2792)
        self.assertEqual(quota_set.gigabytes_ssd['in_use'], 1085)
        self.assertEqual(quota_set.gigabytes_sas['in_use'], 21)
        self.assertEqual(quota_set.gigabytes_sata['in_use'], 168)
        self.assertEqual(quota_set.backups['in_use'], 10)
        self.assertEqual(quota_set.backup_gigabytes['in_use'], 51)
        self.assertEqual(quota_set.volumes['in_use'], 108)
        self.assertEqual(quota_set.volumes_ssd['in_use'], 28)
        self.assertEqual(quota_set.volumes_sas['in_use'], 2)
        self.assertEqual(quota_set.volumes_sata['in_use'], 8)
        self.assertEqual(quota_set.snapshots['in_use'], 6)
        self.assertEqual(quota_set.snapshots_ssd['limit'], -1)
        self.assertEqual(quota_set.snapshots_sas['limit'], -1)
        self.assertEqual(quota_set.snapshots_sata['limit'], -1)

    def test_get_volume(self):
        self.mock_response_json_file_values('volume.json')
        volume_id = '591ac654-26d8-41be-bb77-4f90699d2d41'
        volume = self.proxy.get_volume(volume_id)

        self.assert_session_get_with('volumes/{0}'.format(volume_id))
        self.assertEqual(volume.id, volume_id)
        self.assertEqual(volume.availability_zone, 'az1.dc1')
        self.assertEqual(volume.host, 'az1.dc1#SSD')
        self.assertEqual(volume.is_encrypted, False)
        self.assertEqual(volume.multi_attach, True)
        self.assertEqual(volume.updated_at, '2016-02-03T02:19:29.895237')
        self.assertEqual(volume.is_bootable, False)
        self.assertEqual(volume.metadata['quantityGB'], '40')
        self.assertEqual(volume.links[0]['rel'], 'self')

    def test_create_metadata(self):
        volume_id = 'volume-id'
        metadata = {
            'metadata': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        self.mock_response_json_values(metadata)

        new_metadata = self.proxy.create_volume_metadata(volume_id, **metadata)
        self.assert_session_post_with('volumes/{0}/metadata'.format(volume_id),
                                      json=metadata)

        self.assertEqual('value1', new_metadata.metadata['key1'])

    def test_update_metadata(self):
        volume_id = 'volume-id'
        metadata = {
            'metadata': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        self.mock_response_json_values(metadata)

        updated_metadata = self.proxy.update_volume_metadata(volume_id, **metadata)
        self.assert_session_put_with('volumes/{0}/metadata'.format(volume_id),
                                     json=metadata)
        self.assertEqual('value1', updated_metadata.metadata['key1'])

    def test_update_metadata_with_key(self):
        volume_id = 'volume-id'
        key = 'key1'
        metadata = {
            'meta': {
                'key1': 'value1',
            }
        }
        self.mock_response_json_values(metadata)

        updated_metadata = self.proxy.update_volume_metadata(volume_id, key=key,
                                                             **metadata)
        self.assert_session_put_with('volumes/{0}/metadata/{1}'.
                                     format(volume_id, key), json=metadata)
        self.assertEqual('value1', updated_metadata.meta['key1'])

    def test_delete_metadata(self):
        volume_id = 'volume-id'
        key = 'key1'
        self.proxy.delete_volume_metadata(volume_id, key)
        self.assert_session_delete('volumes/{0}/metadata/{1}'.format(volume_id,
                                                                     key))

    def test_get_metadata(self):
        self.mock_response_json_values({
            'metadata': {
                'key1': 'value1'
            }
        })
        volume_id = 'volume-id'
        metadata = self.proxy.get_volume_metadata(volume_id)
        self.assert_session_get_with('volumes/{0}/metadata'.format(volume_id))
        self.assertEqual('value1', metadata.metadata['key1'])

    def test_get_metadata_with_key(self):
        self.mock_response_json_values({
            'meta': {
                'key1': 'value1'
            }
        })
        key = 'key1'
        volume_id = 'volume-id'
        metadata = self.proxy.get_volume_metadata(volume_id, key)
        self.assert_session_get_with('volumes/{0}/metadata/{1}'.
                                     format(volume_id, key))
        self.assertEqual('value1', metadata.meta[key])

    def test_set_volume_bootable(self):
        volume_id = 'volume-id'
        bootable = True
        json = {
            'os-set_bootable': {
                'bootable': bootable
            }
        }
        self.proxy.set_volume_bootable(volume_id, bootable)
        self.assert_session_post_with('volumes/{0}/action'.format(volume_id),
                                      json=json)

    def test_set_volume_readonly(self):
        volume_id = 'volume-id'
        readonly = True
        json = {
            'os-update_readonly_flag': {
                'readonly': readonly
            }
        }
        self.proxy.set_volume_readonly(volume_id, readonly)
        self.assert_session_post_with('volumes/{0}/action'.format(volume_id),
                                      json=json)

    def test_list_snapshot_details(self):
        self.mock_response_json_file_values('snapshots_detail.json')
        query = {
            'limit': 10
        }
        details = list(self.proxy.snapshots(**query))
        self.assert_session_list_with('/snapshots/detail', params=query)
        self.assertIs(2, len(details))
        snapshot = details[0]
        self.assertEqual('available', snapshot.status)
        self.assertEqual('100%', snapshot.progress)
        self.assertEqual(None, snapshot.description)
        self.assertEqual('2013-06-19T07:15:29.000000', snapshot.created_at)
        self.assertEqual({}, snapshot.metadata)
        self.assertEqual('ae11e59c-bd56-434a-a00c-04757e1c066d', snapshot.volume_id)
        self.assertEqual('d6c277ba8820452e83df36f33c9fa561', snapshot.project_id)
        self.assertEqual(5, snapshot.size)
        self.assertEqual('6cd26877-3ca3-4f4e-ae2a-38cc3d6183fa', snapshot.id)
        self.assertEqual('name_xx2-snap', snapshot.name)
        self.assertEqual(None, snapshot.updated_at)

    def test_create_snapshot(self):
        self.mock_response_json_file_values('snapshot_create.json')
        attr = {
            'name': 'snap-001',
            'description': 'Daily backup',
            'volume_id': '5aa119a8-d25b-45a7-8d1b-88e127885635',
            'force': False,
            'metadata': { }
        }
        expected = {
            'snapshot': attr
        }
        snapshot = self.proxy.create_snapshot(**attr)
        self.assert_session_post_with('/snapshots', json=expected)
        self.assertEqual('creating', snapshot.status)
        self.assertEqual('Daily backup', snapshot.description)
        self.assertEqual('2013-02-25T03:56:53.081642', snapshot.created_at)
        self.assertEqual({}, snapshot.metadata)
        self.assertEqual('5aa119a8-d25b-45a7-8d1b-88e127885635',
                         snapshot.volume_id)
        self.assertEqual(1, snapshot.size)
        self.assertEqual('ffa9bc5e-1172-4021-acaf-cdcd78a9584d', snapshot.id)
        self.assertEqual('snap-001', snapshot.name)
        self.assertEqual('2013-02-25T03:56:53.081642', snapshot.updated_at)

    def test_rollback_snapshot(self):
        snapshot_id = 'snapshot-id'
        volume_id = 'volume-id'
        volume_name = 'volume-name'
        expected = {
            'rollback': {
                'name': volume_name,
                'volume_id': volume_id
            }
        }
        self.mock_response_json_values({
            'rollback': {
                'volume_id': volume_id
            }
        })
        snapshot_rollback = self.proxy.rollback_snapshot(volume_id, volume_name, snapshot_id)
        self.assert_session_post_with('os-vendor-snapshots/{0}/rollback'.
                                      format(snapshot_id),
                                      json=expected)
        self.assertEqual(volume_id, snapshot_rollback.rollback['volume_id'])

    def test_update_snapshot(self):
        snapshot_id = 'snapshot-id'
        attrs = {
            'name': 'name_xx3',
            'description': 'hello'
        }
        self.mock_response_json_file_values('snapshot_update.json')
        snapshot = self.proxy.update_snapshot(snapshot_id, **attrs)
        self.assert_session_put_with('snapshots/{0}'.format(snapshot_id),
                                     json=attrs)
        self.assertEqual(attrs['name'], snapshot.name)
        self.assertEqual(attrs['description'], snapshot.description)
        self.assertEqual('5aa119a8-d25b-45a7-8d1b-88e127885635', snapshot.volume_id)
