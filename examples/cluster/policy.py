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

"""
Managing policies in the Cluster service.

For a full guide see
https://developer.openstack.org/sdks/python/openstacksdk/users/guides/cluster.html
"""


def list_policies(conn):
    print("List Policies:")

    for policy in conn.cluster.policies():
        print(policy.to_dict())

    for policy in conn.cluster.policies(sort='name:asc'):
        print(policy.to_dict())


def create_policy(conn):
    print("Create Policy:")

    spec = {
        'policy': 'senlin.policy.deletion',
        'version': 1.0,
        'properties': {
            'criteria': 'oldest_first',
            'destroy_after_deletion': True,
        }
    }

    policy = conn.cluster.create_policy('dp01', spec)
    print(policy.to_dict())


def get_policy(conn):
    print("Get Policy:")

    policy = conn.cluster.get_policy('dp01')
    print(policy.to_dict())


def find_policy(conn):
    print("Find Policy:")

    policy = conn.cluster.find_policy('dp01')
    print(policy.to_dict())


def update_policy(conn):
    print("Update Policy:")

    policy = conn.cluster.update_policy('dp01', name='dp02')
    print(policy.to_dict())


def delete_policy(conn):
    print("Delete Policy:")

    conn.cluster.delete_policy('dp01')

    print("Policy deleted.")
