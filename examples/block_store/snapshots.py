# Copyright 2017 OpenStack.org
#
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
#      Huawei has modified this source file.
#            Copyright 2018 Huawei Technologies Co., Ltd.
#            Licensed under the Apache License, Version 2.0 (the "License"); you may not
#            use this file except in compliance with the License. You may obtain a copy of
#            the License at
#
#                http://www.apache.org/licenses/LICENSE-2.0
#
#            Unless required by applicable law or agreed to in writing, software
#            distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#            WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#            License for the specific language governing permissions and limitations under
#            the License.

import logging


def snapshots_detail(conn):
    query = {
        'limit': 10
    }
    details = list(conn.block_store.snapshots(**query))
    logging.info(details)


def create_snapshot(conn):
    attr = {
        'name': 'snap-001',
        'description': 'Daily backup',
        'volume_id': '5aa119a8-d25b-45a7-8d1b-88e127885635',
        'force': False,
        'metadata': {}
    }
    snapshot = conn.block_store.create_snapshot(**attr)
    logging.info(snapshot)


def rollback_snapshot(conn):
    snapshot_id = 'snapshot-id'
    volume_id = 'volume-id'
    volume_name = 'volume-name'
    snapshot_rollback = conn.block_store.rollback_snapshot(volume_id,
                                                           volume_name,
                                                           snapshot_id)
    logging.info(snapshot_rollback)


def update_snapshot(conn):
    snapshot_id = 'snapshot-id'
    attrs = {
        'name': 'name_xx3',
        'description': 'hello'
    }
    snapshot = conn.block_store.update_snapshot(snapshot_id, **attrs)
    logging.info(snapshot)


def create_snapshot_metadata(conn):
    snapshot_id = 'snapshot-id'
    metadata = {
        'metadata': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    new_metadata = conn.block_store.create_snapshot_metadata(snapshot_id,
                                                             **metadata)
    logging.info(new_metadata)


def update_snapshot_metadata(conn):
    snapshot_id = 'snapshot-id'
    metadata = {
        'metadata': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    updated_metadata = conn.block_store.update_snapshot_metadata(snapshot_id, **metadata)
    logging.info(updated_metadata)


def update_snapshot_metadata_with_key(conn):
    snapshot_id = 'snapshot-id'
    key = 'key1'
    metadata = {
        'meta': {
            'key1': 'value1',
        }
    }
    updated_metadata = conn.block_store.update_snapshot_metadata(snapshot_id,
                                                                 key=key,
                                                                 **metadata)
    logging.info(updated_metadata)


def delete_snapshot_metadata(conn):
    snapshot_id = 'snapshot-id'
    key = 'key1'
    conn.block_store.delete_snapshot_metadata(snapshot_id, key)


def get_snapshot_metadata(conn):
    snapshot_id = 'snapshot-id'
    metadata = conn.block_store.get_snapshot_metadata(snapshot_id)
    logging.info(metadata)


def get_snapshot_metadata_with_key(conn):
    key = 'key1'
    snapshot_id = 'snapshot-id'
    metadata = conn.block_store.get_snapshot_metadata(snapshot_id, key)
    logging.info(metadata)
