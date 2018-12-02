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

from openstack.block_store.v2 import extension as _extension
from openstack.tests.functional import base


class TestExtension(base.BaseFunctionalTest):

    def test_extensions(self):
        extensions = list(self.conn.block_store.extensions())
        self.assertTrue(len(extensions) > 0)
        self.assertIsInstance(extensions[0], _extension.Extension)
