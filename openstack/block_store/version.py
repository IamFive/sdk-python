# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.block_store import block_store_service
from openstack import resource2


class Version(resource2.Resource):
    resource_key = 'version'
    resources_key = 'versions'
    base_path = '/'
    service = block_store_service.BlockStoreService()

    # capabilities
    allow_list = True

    # Properties
    links = resource2.Body('links', type=list)
    status = resource2.Body('status')

    #: The minimum API version.
    min_version = resource2.Body('min_version')
    #: The request messages type of the API version.
    media_types = resource2.Body('media-types', type=list)
    #: The ID of the API version.
    id = resource2.Body('id')
    #: The last time when the API version is updated.
    updated = resource2.Body('updated')
    #: The sub-version of the API version.
    version = resource2.Body('version')


class VersionV2(Version):
    base_path = '/v2'
