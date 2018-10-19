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

from openstack.block_store import block_store_service
from openstack import format
from openstack import resource2
from openstack import utils


class Volume(resource2.Resource):
    resource_key = "volume"
    resources_key = "volumes"
    base_path = "/volumes"
    service = block_store_service.BlockStoreService()

    _query_mapping = resource2.QueryParameters('all_tenants', 'name',
                                               'status', 'project_id')

    # capabilities
    allow_get = True
    allow_create = True
    allow_delete = True
    allow_update = True
    allow_list = True

    # Properties
    #: A ID representing this volume.
    id = resource2.Body("id")
    #: The name of this volume.
    name = resource2.Body("name")
    #: A list of links associated with this volume. *Type: list*
    links = resource2.Body("links", type=list)

    #: The availability zone.
    availability_zone = resource2.Body("availability_zone")
    #: To create a volume from an existing volume, specify the ID of
    #: the existing volume. If specified, the volume is created with
    #: same size of the source volume.
    source_volume_id = resource2.Body("source_volid")
    #: The volume description.
    description = resource2.Body("description")
    #: To create a volume from an existing snapshot, specify the ID of
    #: the existing volume snapshot. If specified, the volume is created
    #: in same availability zone and with same size of the snapshot.
    snapshot_id = resource2.Body("snapshot_id")
    #: The size of the volume, in GBs. *Type: int*
    size = resource2.Body("size", type=int)
    #: The ID of the image from which you want to create the volume.
    #: Required to create a bootable volume.
    image_id = resource2.Body("imageRef")
    #: The name of the associated volume type.
    volume_type = resource2.Body("volume_type")
    #: Enables or disables the bootable attribute. You can boot an
    #: instance from a bootable volume. *Type: bool*
    is_bootable = resource2.Body("bootable", type=format.BoolStr)
    #: One or more metadata key and value pairs to associate with the volume.
    metadata = resource2.Body("metadata")

    #: One of the following values: creating, available, attaching, in-use
    #: deleting, error, error_deleting, backing-up, restoring-backup,
    #: error_restoring. For details on these statuses, see the
    #: Block Storage API documentation.
    status = resource2.Body("status")
    #: TODO(briancurtin): This is currently undocumented in the API.
    attachments = resource2.Body("attachments")
    #: The timestamp of this volume creation.
    created_at = resource2.Body("created_at")

    #: The project ID associated with current back-end.
    project_id = resource2.Body("os-vol-tenant-attr:tenant_id")
    #: The metadata of the EVS disk image.
    volume_image_metadata = resource2.Body('volume_image_metadata', type=dict)
    #: The volume's current back-end.
    host = resource2.Body("os-vol-host-attr:host")
    #: ``True`` if this volume is encrypted, ``False`` if not.
    #: *Type: bool*
    is_encrypted = resource2.Body("encrypted", type=format.BoolStr)
    #: The time when the EVS disk information was updated.
    updated_at = resource2.Body('updated_at')
    #: Extended replication status on this volume.
    extended_replication_status = resource2.Body(
        "os-volume-replication:extended_status")
    #: Status of replication on this volume.
    replication_status = resource2.Body("replication_status")
    #: The status of this volume's migration (None means that a migration
    #: is not currently in progress).
    migration_status = resource2.Body("os-vol-mig-status-attr:migstat")
    #: ID of the consistency group.
    consistency_group_id = resource2.Body("consistencygroup_id")
    #: The volume ID that this volume's name on the back-end is based on.
    migration_id = resource2.Body("os-vol-mig-status-attr:name_id")
    #: Whether the EVS disk is shareable.
    shareable = resource2.Body('shareable', type=bool)
    #: Reserved.
    user_id = resource2.Body('user_id')
    #: The shared EVS disk information.
    multi_attach = resource2.Body('multiattach', type=bool)


class VolumeDetail(Volume):

    base_path = "/volumes/detail"

    #: The volume's current back-end.
    host = resource2.Body("os-vol-host-attr:host")
    #: The project ID associated with current back-end.
    project_id = resource2.Body("os-vol-tenant-attr:tenant_id")
    #: The status of this volume's migration (None means that a migration
    #: is not currently in progress).
    migration_status = resource2.Body("os-vol-mig-status-attr:migstat")
    #: The volume ID that this volume's name on the back-end is based on.
    migration_id = resource2.Body("os-vol-mig-status-attr:name_id")
    #: Status of replication on this volume.
    replication_status = resource2.Body("replication_status")
    #: Extended replication status on this volume.
    extended_replication_status = resource2.Body(
        "os-volume-replication:extended_status")
    #: ID of the consistency group.
    consistency_group_id = resource2.Body("consistencygroup_id")
    #: Data set by the replication driver
    replication_driver_data = resource2.Body(
        "os-volume-replication:driver_data")
    #: ``True`` if this volume is encrypted, ``False`` if not.
    #: *Type: bool*
    is_encrypted = resource2.Body("encrypted", type=format.BoolStr)


class QuotaSet(resource2.Resource):
    resource_key = 'quota_set'
    base_path = '/os-quota-sets/%(tenant_id)s?usage=True'
    service = block_store_service.BlockStoreService()

    # capabilities
    allow_get = True

    # URI parameters
    tenant_id = resource2.URI('tenant_id')

    #: Properties
    #: The number of EVS disksevs_service
    volumes = resource2.Body('volumes', type=dict)
    #: The number of snapshots
    snapshots = resource2.Body('snapshots', type=dict)
    #: The total size (GB) of EVS disks and snapshots allowed by the quota
    gigabytes = resource2.Body('gigabytes', type=dict)
    #: The number of EVS disks reserved for a specified volume type
    volumes_sata = resource2.Body('volumes_SATA', type=dict)
    volumes_ssd = resource2.Body('volumes_SSD', type=dict)
    volumes_sas = resource2.Body('volumes_SAS', type=dict)
    #: The number of snapshots reserved for a specified volume type
    snapshots_sata = resource2.Body('snapshots_SATA', type=dict)
    snapshots_ssd = resource2.Body('snapshots_SSD', type=dict)
    snapshots_sas = resource2.Body('snapshots_SAS', type=dict)
    #: The size (GB) reserved for a specified volume type
    gigabytes_sata = resource2.Body('gigabytes_SATA', type=dict)
    gigabytes_ssd = resource2.Body('gigabytes_SSD', type=dict)
    gigabytes_sas = resource2.Body('gigabytes_SAS', type=dict)
    #: Tenant ID
    id = resource2.Body('id')
    #: The number of backups
    backups = resource2.Body('backups', type=dict)
    #: The backup size (GB)
    backup_gigabytes = resource2.Body('backup_gigabytes', type=dict)


class VolumeMetadata(resource2.Resource):
    base_path = '/volumes'
    service = block_store_service.BlockStoreService()

    # capabilities
    allow_get = True
    allow_update = True
    allow_delete = True

    # properties
    #: EVS disk metadata
    meta = resource2.Body('meta', type=dict)
    metadata = resource2.Body('metadata', type=dict)

    def _operate_metadata(self, method, url, has_body=True, **kwargs):
        request = self._prepare_request(requires_id=False)
        request.uri = url
        endpoint_override = self.service.get_endpoint_override()
        response = method(request.uri,
                          endpoint_filter=self.service,
                          endpoint_override=endpoint_override,
                          **kwargs)
        self._translate_response(response, has_body)
        return self

    def create_metadata(self, session, volume_id, metadata):
        url = utils.urljoin(self.base_path, volume_id, 'metadata')
        d = {
            'json': metadata,
            'headers': {},
        }
        return self._operate_metadata(session.post, url, **d)

    def update_metadata(self, session, volume_id, metadata, key=None):
        if key:
            url = utils.urljoin(self.base_path, volume_id, 'metadata', key)
        else:
            url = utils.urljoin(self.base_path, volume_id, 'metadata')
        if key and metadata.get('meta'):
            for k in list(metadata['meta'].keys()):
                if not k == key:
                    del metadata[k]
        d = {
            'json': metadata,
            'headers': {},
        }
        return self._operate_metadata(session.put, url, **d)

    def delete_metadata(self, session, volume_id, key):
        url = utils.urljoin(self.base_path, volume_id, 'metadata', key)
        d = {
            'headers': {'Accept': ''},
            'params': None
        }
        self._operate_metadata(session.delete, url, has_body=False, **d)

    def get_metadata(self, session, volume_id, key=None):
        if key:
            url = utils.urljoin(self.base_path, volume_id, 'metadata', key)
        else:
            url = utils.urljoin(self.base_path, volume_id, 'metadata')
        return self._operate_metadata(session.get, url)
