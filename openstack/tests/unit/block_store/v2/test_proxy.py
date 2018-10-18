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
