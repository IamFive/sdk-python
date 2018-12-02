# Copyright 2018 Huawei Technologies Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

import logging


def get_quota_set(conn):
    tenant_id = 'some-tenant-id'
    quota_set = conn.block_store.get_quota_set(tenant_id)
    for qs in quota_set:
        logging.info(qs)


def volumes(conn):
    volumes = conn.block_store.volumes(details=False)
    for v in volumes:
        logging.info(v)


def get_volume(conn):
    volume = conn.block_store.get_volume('some-volume-id')
    logging.info(volume)


def create_volume_metadata(conn):
    attrs = {
        'metadata': {
            'key1': 'value1'
        }
    }
    metadata = conn.block_store.create_volume_metadata('some-volume-id',
                                                       **attrs)
    logging.info(metadata)


def update_volume_metadata(conn):
    volume_id = 'some-volume-id'
    metadata = {
        'metadata': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    updated_metadata = conn.block_store.update_volume_metadata(volume_id,
                                                               **metadata)
    logging.info(updated_metadata)


def update_volume_metadata_with_key(conn):
    volume_id = 'volume-id'
    key = 'key1'
    metadata = {
        'meta': {
            'key1': 'value1',
        }
    }

    updated_metadata = conn.block_store.update_volume_metadata(volume_id,
                                                               key=key,
                                                               **metadata)
    logging.info(updated_metadata)


def delete_volume_metadata(conn):
    volume_id = 'volume-id'
    key = 'key1'
    conn.block_store.delete_volume_metadata(volume_id, key)


def get_volume_metadata(conn):
    volume_id = 'volume-id'
    metadata = conn.block_store.get_volume_metadata(volume_id)
    logging.info(metadata)


def get_volume_metadata_with_key(conn):
    key = 'key1'
    volume_id = 'volume-id'
    metadata = conn.block_store.get_volume_metadata(volume_id, key)
    logging.info(metadata)


def set_volume_bootable(conn):
    volume_id = 'volume-id'
    bootable = True
    conn.block_store.set_volume_bootable(volume_id, bootable)


def set_volume_readonly(conn):
    volume_id = 'volume-id'
    readonly = True
    conn.block_store.set_volume_readonly(volume_id, readonly)
