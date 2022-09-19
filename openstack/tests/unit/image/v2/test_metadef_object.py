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

import io
import operator
import tempfile
from unittest import mock

from keystoneauth1 import adapter
import requests

from openstack import _log
from openstack import exceptions
from openstack.image.v2 import metadef_object as _metadef_object
from openstack.tests.unit import base
from openstack import utils

EXAMPLE = {
    'created_at': '2022-09-02T01:05:00Z',
    'name': 'foo',
    'description': 'create new test object',
    'namespace': 'test-namespace',
    'properties': '[\'apple\', \'banana\']',
    'required': [],
    'schema': '/v2/schemas/metadefs/object',
    'updated_at': '2022-09-02T01:10:00Z'
}


class FakeResponse:
    def __init__(self, response, status_code=200, headers=None, reason=None):
        self.body = response
        self.content = response
        self.text = response
        self.status_code = status_code
        headers = headers if headers else {'content-type': 'application/json'}
        self.headers = requests.structures.CaseInsensitiveDict(headers)
        if reason:
            self.reason = reason
        # for the sake of "list" response faking
        self.links = []

    def json(self):
        return self.body


class TestMetadefObject(base.TestCase):

    def setUp(self):
        super(TestMetadefObject, self).setUp()
        self.resp = mock.Mock()
        self.resp.body = None
        self.resp.json = mock.Mock(return_value=self.resp.body)
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock(return_value=self.resp)
        self.sess.put = mock.Mock(return_value=FakeResponse({}))
        self.sess.delete = mock.Mock(return_value=FakeResponse({}))
        self.sess.get = mock.Mock(return_value=FakeResponse({}))
        self.sess.default_microversion = None
        self.sess.retriable_status_codes = None
        self.sess.log = _log.setup_logging('openstack')

    def test_basic(self):
        sot = _metadef_object.MetadefObject()
        self.assertEqual('/metadefs/namespaces', sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)

        self.assertDictEqual(
            {
                'created_at': 'created_at',
                'name': 'name',
                'limit': 'limit',
                'marker': 'marker',
                'description': 'description',
                'namespace': 'namespace',
                'properties': 'properties',
                'required': 'required',
                'schema': 'schema',
                'updated_at': 'updated_at'
            },
            sot._query_mapping._mapping,
        )

    def test_create(self):
        sot = _metadef_object.MetadefObject(**EXAMPLE)
        sot.create(self.sess)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['namespace'], sot.namespace)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['properties'], sot.properties)
        self.assertEqual(EXAMPLE['required'], sot.required)
        self.assertEqual(EXAMPLE['schema'], sot.schema)
        self.sess.post.assert_called_with('metadefs/namespaces/'+ EXAMPLE['namespace']+'/objects', json={'name': EXAMPLE['name'], 'properties': EXAMPLE['properties']})

