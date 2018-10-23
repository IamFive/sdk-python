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

from openstack.block_store.v2 import snapshot as _snapshot
from openstack.block_store.v2 import volume as _volume
from openstack.tests.functional import base


class TestSnapshot(base.BaseFunctionalTest):

    SNAPSHOT_NAME = uuid.uuid4().hex
    SNAPSHOT_ID = None
    VOLUME_NAME = uuid.uuid4().hex
    VOLUME_ID = None
    SNAPSHOT_METADATA_KEY = 'key1'
    SNAPSHOT_METADATA_VALUE = 'value1'

    @classmethod
    def setUpClass(cls):
        super(TestSnapshot, cls).setUpClass()
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
        snapshot = cls.conn.block_store.create_snapshot(
            name=cls.SNAPSHOT_NAME,
            volume_id=cls.VOLUME_ID)
        cls.conn.block_store.wait_for_status(snapshot,
                                             status='available',
                                             failures=['error'],
                                             interval=2,
                                             wait=120)
        assert isinstance(snapshot, _snapshot.Snapshot)
        cls.assertIs(cls.SNAPSHOT_NAME, snapshot.name)
        attrs = {
            'metadata': {
                cls.SNAPSHOT_METADATA_KEY: cls.SNAPSHOT_METADATA_VALUE
            }
        }
        snapshot_metadata = \
            cls.conn.block_store.create_snapshot_metadata(snapshot.id, **attrs)
        assert isinstance(snapshot_metadata, _snapshot.SnapshotMetadata)

        cls.SNAPSHOT_ID = snapshot.id

    @classmethod
    def tearDownClass(cls):
        ret = cls.conn.block_store.delete_snapshot_metadata(
            cls.SNAPSHOT_ID, key=cls.SNAPSHOT_METADATA_KEY, ignore_missing=False)
        cls.assertIs(None, ret)

        snapshot = cls.conn.block_store.get_snapshot(cls.SNAPSHOT_ID)
        sot = cls.conn.block_store.delete_snapshot(snapshot,
                                                   ignore_missing=False)
        cls.conn.block_store.wait_for_delete(snapshot,
                                             interval=2,
                                             wait=120)
        cls.assertIs(None, sot)
        volume = cls.conn.block_store.get_volume(cls.VOLUME_ID)
        cls.conn.block_store.wait_for_status(volume,
                                             status='available',
                                             failures=['error'],
                                             interval=2,
                                             wait=120)
        sot = cls.conn.block_store.delete_volume(cls.VOLUME_ID,
                                                 ignore_missing=False)
        cls.assertIs(None, sot)

    def test_get(self):
        sot = self.conn.block_store.get_snapshot(self.SNAPSHOT_ID)
        self.assertEqual(self.SNAPSHOT_NAME, sot.name)

    def test_snapshots(self):
        query = {
            'limit': 10
        }
        snapshots = \
            list(self.conn.block_store.snapshots(details=True, **query))
        snapshot_ids = [s.id for s in snapshots]
        self.assertTrue(self.SNAPSHOT_ID in snapshot_ids)

    def test_update_snapshot(self):
        new_name = 'snapshot new name'
        new_desc = 'new desc'
        attrs = {
            'name': new_name,
            'description': new_desc
        }
        snapshot = \
            self.conn.block_store.update_snapshot(self.SNAPSHOT_ID, **attrs)
        self.assertIsInstance(snapshot, _snapshot.Snapshot)
        self.assertEqual(new_name, snapshot.name)
        self.assertEqual(new_desc, snapshot.description)

    def test_get_snapshot_metadata(self):
        snapshot = \
            self.conn.block_store.get_snapshot_metadata(self.SNAPSHOT_ID)
        self.assertIsInstance(snapshot, _snapshot.SnapshotMetadata)
        self.assertEqual(self.SNAPSHOT_METADATA_VALUE,
                         snapshot.metadata[self.SNAPSHOT_METADATA_KEY])

    def test_update_snapshot_metadata(self):
        new_value = 'new value'
        attrs = {
            'metadata': {
                self.SNAPSHOT_METADATA_KEY: new_value
            }
        }
        metadata = self.conn.block_store.update_snapshot_metadata(
            self.SNAPSHOT_ID, **attrs)
        self.assertIsInstance(metadata, _snapshot.SnapshotMetadata)
        self.assertEqual(new_value,
                         metadata.metadata[self.SNAPSHOT_METADATA_KEY])

    def test_get_snapshot_metadata_with_key(self):
        snapshot = self.conn.block_store.get_snapshot_metadata(
            self.SNAPSHOT_ID, key=self.SNAPSHOT_METADATA_KEY)
        self.assertIsInstance(snapshot, _snapshot.SnapshotMetadata)
        self.assertEqual(self.SNAPSHOT_METADATA_VALUE,
                         snapshot.meta[self.SNAPSHOT_METADATA_KEY])

    def test_update_snapshot_metadata_with_key(self):
        new_value = 'new value'
        attrs = {
            'meta': {
                self.SNAPSHOT_METADATA_KEY: new_value
            }
        }
        snapshot_metadata = self.conn.block_store.update_snapshot_metadata(
            self.SNAPSHOT_ID, key=self.SNAPSHOT_METADATA_KEY, **attrs)
        self.assertIsInstance(snapshot_metadata, _snapshot.SnapshotMetadata)
        self.assertEqual(new_value,
                         snapshot_metadata.meta[self.SNAPSHOT_METADATA_KEY])

    def test_rollback_snapshot(self):
        rollback = self.conn.block_store.rollback_snapshot(self.VOLUME_ID,
                                                           self.VOLUME_NAME,
                                                           self.SNAPSHOT_ID)
        self.assertIsInstance(rollback, _snapshot.SnapshotRollback)
        self.assertEqual(self.VOLUME_ID, rollback.rollback['volume_id'])
