from openstack.common import tag
from openstack import exceptions
from openstack.image import _download
from openstack import resource
from openstack import utils
import json


class MetadefObject(resource.Resource):
    base_path = '/metadefs/namespaces/%(namespace_name)s/objects'

    # capabilities
    allow_create = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "namespace_name",
        "name",
        "description",
        "properties",
        "required"
    )

    # response
    namespace = resource.URI('namespace_name')

    created_at = resource.Body('created_at')
    name = resource.Body('name')
    description = resource.Body('description')
    properties = resource.Body('properties')
    required = resource.Body('required')
    updated_at = resource.Body('updated_at')
    schema = resource.Body('schema')
