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
            'attrs': v.get('properties', {}).get('attrs', {})
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


def _check_is_adf_node(input_item):
    return ADFObject in type(input_item).__mro__


class ADFObject(object):
    def __init__(self, node_type, chain_mode=True):
        """
        Node/Mark Object in an Atlassian Document.
        :param node_type: Define the type of the node.
        :param chain_mode: Specify which node to be returned after calling add()
            chain_mode: True  -> Return Original Node
            chain_mode: False -> Return the new Node
        """
        node_list, mark_list = adf_node_list(), adf_mark_list()
        self.chain_mode = chain_mode

        self.type = node_type
        self.is_node, self.is_mark = self.type in node_list, self.type in mark_list
        if not self.is_node and not self.is_mark:
            raise RuntimeError(f'{node_type} does not exists in the schema.')

        self._object_list = node_list if self.is_node else mark_list
        self._local_info = {
            prop_key: {'array': list, 'object': dict}.get(prop_type, lambda: None)()
            for prop_key, prop_type in self._object_list[self.type]['prop'].items()
        }

    def add(self, key_or_node, chain_mode=None, **kwargs):
        """
        Add a node to the current node.
        :param key_or_node: Key of the new node or existing node created.
        :param chain_mode: Chain Mode of the new node created by key. Existing node not affected.
        :param kwargs:
        :return: self.chain_mode ? Current node : New Node
        """
        self._check_if_node_has_children()
        new_chain_mode = self.chain_mode if chain_mode is None else chain_mode
        new_node = ADFObject(key_or_node, chain_mode=new_chain_mode) if not _check_is_adf_node(
            key_or_node) else key_or_node
        self._local_info['content'].append(new_node)
        return self if self.chain_mode else new_node

    def extend_content(self, nodes):
        """
        Add a list of existing nodes to the current node.
        :param nodes: List of input nodes
        :return: Current Node
        """
        self._check_if_node_has_children()
        nodes = [nodes] if not isinstance(nodes, list) else nodes
        if any(not _check_is_adf_node(node) for node in nodes):
            raise RuntimeError('Input must only contains ADFObject.')
        self._local_info['content'].extend(nodes)
        return self

    def render(self):
        """
        Build a dictionary object with the current node and all the nodes under it.
        :return: dict
        """
        current_level = {
            prop_key: prop_value
            for prop_key, prop_value in self._local_info.items()
            if prop_value is not None and (
                    not isinstance(prop_value, dict) or not isinstance(prop_value, list) or len(prop_value) > 0
            ) and prop_key not in {'type', 'content'}
        }
        current_level['type'] = self.type
        if 'content' in self._local_info:
            current_level['content'] = [child_node.render() for child_node in self._local_info['content']]
        if 'marks' in self._local_info:
            current_level['marks'] = [child_node.render() for child_node in self._local_info['marks']]
        return current_level

    def assign_info(self, field, *values, **kwargs):
        """
        Assign value to field. Extend if the field is a list. Update if the field is a dict.
        :param field: Specified the field to be edited.
        :param values: Value to be added. List accepts multiple values.
        :param kwargs: Values to be added to a dict.
        :return: Current Node
        """
        if field not in self._local_info:
            raise KeyError(f'"{field}" does not exists in the node "{self.type}"')
        if field == 'content':
            raise ValueError(f'"{field}" is protected. Do not modify it with assign_info()')

        if isinstance(self._local_info[field], list):
            if len(values) == 0:
                raise RuntimeError("Field specified without specifying any value.")
            self._local_info[field].extend(list(values))

        elif isinstance(self._local_info[field], dict):
            if len(kwargs) > 0:
                self._local_info[field].update(kwargs)

        else:
            if len(values) != 1:
                raise RuntimeError(f'Specify 1 value for the field "{field}"')
            self._local_info[field] = values[0]

        return self

    def _check_if_node_has_children(self):
        if 'content' not in self._local_info:
            raise RuntimeError(f'"{self.type}" node does not have the filed "content" for adding sub-nodes.')


class ADFDoc(ADFObject):
    def __init__(self, chain_mode=True):
        super(ADFDoc, self).__init__('doc', chain_mode=chain_mode)
        self._local_info['version'] = 1

    def validate(self):
        """
        Validate the output object with the ADF Schema. Raise Exception when validation fails.
        :return: None
        """
        return jsonschema.validate(self.render(), adf_schema())
