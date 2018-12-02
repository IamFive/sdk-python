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

import uuid

from openstack.block_store.v2 import volume as _volume
from openstack.tests.functional import base


class TestVolume(base.BaseFunctionalTest):

    VOLUME_NAME = uuid.uuid4().hex
    VOLUME_ID = None
    VOLUME_METADATA_KEY = 'key1'
    VOLUME_METADATA_VALUE = 'value1'

    @classmethod
    def setUpClass(cls):
        super(TestVolume, cls).setUpClass()
        volume = cls.conn.block_store.create_volume(
            name=cls.VOLUME_NAME,
            size=1)
        cls.conn.block_store.wait_for_status(volume,
                                             status='available',
                                             failures=['error'],
                                             interval=2,
                                             wait=120)
        assert isinstance(volume, _volume.Volume)
        cls.assertIs(cls.VOLUME_NAME, volume.name)
        cls.VOLUME_ID = volume.id

    @classmethod
    def tearDownClass(cls):
        sot = cls.conn.block_store.delete_volume_metadata(cls.VOLUME_ID, key=cls.VOLUME_METADATA_KEY)
        cls.assertIs(None, sot)

        sot = cls.conn.block_store.delete_volume(cls.VOLUME_ID,
                                                 ignore_missing=False)
        cls.assertIs(None, sot)

    def test_get(self):
        sot = self.conn.block_store.get_volume(self.VOLUME_ID)
        self.assertEqual(self.VOLUME_NAME, sot.name)

    def test_get_quota_set(self):
        tenant_id = self.conn.session.auth._project_id
        quota_set = self.conn.block_store.get_quota_set(tenant_id)
        self.assertIsInstance(quota_set, _volume.QuotaSet)
        self.assertEqual(tenant_id, quota_set.tenant_id)

    def test_volumes(self):
        volumes = list(self.conn.block_store.volumes(details=False))
        volume_ids = [v.id for v in volumes]
        self.assertTrue(self.VOLUME_ID in volume_ids)

    def test_create_volume_metadata(self):
        attrs = {
            'metadata': {
                self.VOLUME_METADATA_KEY: self.VOLUME_METADATA_VALUE
            }
        }
        metadata = self.conn.block_store.create_volume_metadata(self.VOLUME_ID, **attrs)
        self.assertIsInstance(metadata, _volume.VolumeMetadata)
        self.assertEqual(self.VOLUME_METADATA_VALUE, metadata.metadata[self.VOLUME_METADATA_KEY])

    def test_get_volume_metadata(self):
        metadata = self.conn.block_store.get_volume_metadata(self.VOLUME_ID)
        self.assertIsInstance(metadata, _volume.VolumeMetadata)
        self.assertEqual(self.VOLUME_METADATA_VALUE, metadata.metadata[self.VOLUME_METADATA_KEY])

    def test_get_volume_metadata_with_key(self):
        metadata = self.conn.block_store.get_volume_metadata(self.VOLUME_ID, key=self.VOLUME_METADATA_KEY)
        self.assertIsInstance(metadata, _volume.VolumeMetadata)
        self.assertEqual(self.VOLUME_METADATA_VALUE, metadata.meta[self.VOLUME_METADATA_KEY])

    def test_update_volume_metadata(self):
        new_value = 'new value'
        attrs = {
            'metadata': {
                self.VOLUME_METADATA_KEY: new_value
            }
        }
        metadata = self.conn.block_store.update_volume_metadata(self.VOLUME_ID, **attrs)
        self.assertIsInstance(metadata, _volume.VolumeMetadata)
        self.assertEqual(new_value, metadata.metadata[self.VOLUME_METADATA_KEY])

    def test_update_volume_metadata_with_key(self):
        new_value = 'new value 2'
        attrs = {
            'meta': {
                self.VOLUME_METADATA_KEY: new_value
            }
        }
        metadata = self.conn.block_store.update_volume_metadata(self.VOLUME_ID, key=self.VOLUME_METADATA_KEY, **attrs)
        self.assertIsInstance(metadata, _volume.VolumeMetadata)
        self.assertEqual(new_value, metadata.meta[self.VOLUME_METADATA_KEY])

    def test_set_volume_bootable(self):
        ret = self.conn.block_store.set_volume_bootable(self.VOLUME_ID, True)
        self.assertIsNone(ret)

    def test_set_volume_readonly(self):
        ret = self.conn.block_store.set_volume_readonly(self.VOLUME_ID, True)
        self.assertIsNone(ret)
