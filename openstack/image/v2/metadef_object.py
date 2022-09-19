from openstack.common import tag
from openstack import exceptions
from openstack.image import _download
from openstack import resource
from openstack import utils
import json


class MetadefObject(resource.Resource):
    base_path = '/metadefs/namespaces'

    # capabilities
    allow_create = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "namespace", "name", "description", "properties",
        "required", "schema"
    )

    created_at = resource.Body('created_at')
    namespace = resource.Body('namespace')
    name = resource.Body('name')
    description = resource.Body('description')
    properties = resource.Body('properties')
    required = resource.Body('required')
    updated_at = resource.Body('updated_at')
    schema = resource.Body('schema')

    data = dict()

    def create(self, session, prepend_key=True, base_path=None, **params):
        url = utils.urljoin(self.base_path, self.namespace, 'objects')
        self.data['name'] = self.name
        self.data['properties'] = json.loads(self.properties)
        return session.post(url, json=self.data)

