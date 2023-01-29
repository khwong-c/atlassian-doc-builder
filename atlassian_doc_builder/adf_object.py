import json
import urllib.request
from functools import cache

import jsonschema


@cache
def adf_schema():
    with urllib.request.urlopen('https://go.atlassian.com/adf-json-schema') as response:
        return json.load(response)


def _decode_schema_with_filter(schema, filter_expression):
    return {
        v['properties']['type']['enum'][0]: {
            'prop': {
                prop_key: prop_detail.get('type', 'string') if prop_key not in ('attrs', 'content') else
                {'attrs': 'object', 'content': 'array'}[prop_key]

                for prop_key, prop_detail in v.get('properties', {}).items()
                if prop_key != 'type'
            },
            'required': tuple(v.get('required', [])),
            'attrs': tuple(v.get('properties', {}).get('attrs', {}).get('properties', {}).keys()),
        }
        for k, v in schema['definitions'].items()
        if filter_expression(k, v)
    }


@cache
def adf_mark_list():
    return _decode_schema_with_filter(
        adf_schema(),
        lambda key, value: 'mark' in key[-4:]
    )


@cache
def adf_node_list():
    return _decode_schema_with_filter(
        adf_schema(),
        lambda key, value: 'node' in key[-4:] and 'type' in value
    )


class ADFObject(object):
    def __init__(self, node_type, chain_mode=True):
        node_list, mark_list = adf_node_list(), adf_mark_list()

        # Specify which node to be returned after calling add()
        self.chain_mode = chain_mode

        self.type = node_type
        self.is_node, self.is_mark = self.type in node_list, self.type in mark_list
        if not self.is_node and not self.is_mark:
            raise RuntimeError(f'{node_type} does not exists in the schema.')

        self._object_list = node_list if self.is_node else mark_list
        self.local_info = {
            prop_key: {'array': list, 'object': dict}.get(prop_type, lambda: None)()
            for prop_key, prop_type in self._object_list[self.type]['prop'].items()
        }

    def add(self):
        pass

    def extend_content(self):
        pass

    def render(self):
        pass

    def assign_info(self, field, **kwargs):
        pass


class ADFDoc(ADFObject):
    def __init__(self, chain_mode=True):
        super(ADFDoc, self).__init__('doc', chain_mode=chain_mode)
        self.local_info['version'] = 1

    def validate(self):
        """
        Validate the output object with the ADF Schema. Raise Exception when validation fails.
        :return: None
        """
        return jsonschema.validate(self.render(), adf_schema())
