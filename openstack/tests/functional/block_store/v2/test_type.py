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
#     Huawei has modified this source file.
#
#             Copyright 2018 Huawei Technologies Co., Ltd.
#
#             Licensed under the Apache License, Version 2.0 (the "License"); you may not
#             use this file except in compliance with the License. You may obtain a copy of
#             the License at
#
#                  http://www.apache.org/licenses/LICENSE-2.0
#
#             Unless required by applicable law or agreed to in writing, software
#             distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#             WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#             License for the specific language governing permissions and limitations under
#             the License.

import uuid

from openstack.block_store.v2 import type as _type
from openstack.tests.functional import base


class TestType(base.BaseFunctionalTest):

    TYPE_NAME = uuid.uuid4().hex
    TYPE_ID = None

    @classmethod
    def setUpClass(cls):
        super(TestType, cls).setUpClass()
        types = list(cls.conn.block_store.types())
        cls.assertIs(True, len(types) > 0)
        type = types[0]
        cls.assertIs(True, isinstance(type, _type.Type))
        cls.TYPE_ID = type.id
        cls.TYPE_NAME = type.name
        # super(TestType, cls).setUpClass()
        # sot = cls.conn.block_store.create_type(name=cls.TYPE_NAME)
        # assert isinstance(sot, _type.Type)
        # cls.assertIs(cls.TYPE_NAME, sot.name)
        # cls.TYPE_ID = sot.id

    # @classmethod
    # def tearDownClass(cls):
    #     sot = cls.conn.block_store.delete_type(cls.TYPE_ID,
    #                                            ignore_missing=False)
    #     cls.assertIs(None, sot)

    def test_get(self):
        sot = self.conn.block_store.get_type(self.TYPE_ID)
        self.assertEqual(self.TYPE_NAME, sot.name)

    def test_types(self):
        types = list(self.conn.block_store.types())
        self.assertTrue(len(types) > 0)
        self.assertIsInstance(types[0], _type.Type)
