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

import os

from openstack.block_store import version as _version
from openstack.tests.functional import base


class TestVersion(base.BaseFunctionalTest):

    def test_versions(self):
        os.environ.setdefault(
            'OS_VOLUME_ENDPOINT_OVERRIDE',
            'https://evs.cn-north-1.myhuaweicloud.com'
        )
        versions = list(self.conn.block_store.versions())
        self.assertTrue(len(versions) > 0)
        self.assertIsInstance(versions[0], _version.Version)

    def test_versions_v2(self):
        os.environ.setdefault(
            'OS_VOLUME_ENDPOINT_OVERRIDE',
            'https://evs.cn-north-1.myhuaweicloud.com'
        )
        versions = list(self.conn.block_store.versions(v2=True))
        self.assertTrue(len(versions) > 0)
        self.assertIsInstance(versions[0], _version.VersionV2)
