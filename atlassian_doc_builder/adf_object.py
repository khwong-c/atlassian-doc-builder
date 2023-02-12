import json
import re
import urllib.request
from functools import lru_cache as cache

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


class ADFObject(object):
    PATTERN_EXP, PATTERN_VAR = re.compile('\{[^\}]+\}'), re.compile('[0-9a-zA-Z_]+')

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
        self._parent = None

        self.type = node_type
        self.is_node, self.is_mark = self.type in node_list, self.type in mark_list
        if not self.is_node and not self.is_mark:
            raise RuntimeError(f'{node_type} does not exists in the schema.')

        self._object_list = node_list if self.is_node else mark_list
        self.local_info = {
            prop_key: {'array': list, 'object': dict}.get(prop_type, lambda: None)()
            for prop_key, prop_type in self._object_list[self.type]['prop'].items()
        }

    @property
    def parent(self):
        return self._parent

    def add(self, key_or_node, chain_mode=None, **kwargs):
        """
        Add a node to the current node.
        :param key_or_node: Key of the new node or existing node created.
        :param chain_mode: Chain Mode of the new node created by key. Existing node not affected.
        :param kwargs:
        :return: self.chain_mode ? Current node : New Node
        """
        new_chain_mode = self.chain_mode if chain_mode is None else chain_mode
        new_node = key_or_node if issubclass(type(key_or_node), ADFObject) else ADFObject(key_or_node,
                                                                                          chain_mode=new_chain_mode)
        new_node._parent = self

        if new_node.is_mark:
            if 'marks' not in self.local_info:
                raise ValueError(f'Adding a mark: {new_node.type} to node: {self.type} is forbidden.')
            self.local_info['marks'].append(new_node)
        if new_node.is_node:
            if 'content' not in self.local_info:
                raise ValueError(f'Adding a node: {new_node.type} to node: {self.type} is forbidden.')
            self.local_info['content'].append(new_node)
        return self if self.chain_mode else new_node

    def extend_content(self, nodes):
        """
        Add a list of existing nodes to the current node. Marks are not allowed.
        :param nodes: List of input nodes
        :return: Current Node
        """
        if 'content' not in self.local_info:
            raise RuntimeError(f'"{self.type}" node does not have the filed "content" for adding sub-nodes.')

        nodes = [nodes] if not isinstance(nodes, list) else nodes
        if any(not issubclass(type(node), ADFObject) or not node.is_node for node in nodes):
            raise RuntimeError('Input must only contains ADFObject.')
        self.local_info['content'].extend(nodes)
        return self

    def render(self):
        """
        Build a dictionary object with the current node and all the nodes under it.
        :return: dict
        """
        # BFS Rendering.
        # Marks does not have further child node. Recursive call accepted.
        render_queue, top_node_rendered = [(self, None)], None
        while render_queue:
            cur_node, parent_node = render_queue.pop(0)
            current_level_rendered = {
                prop_key: prop_value
                for prop_key, prop_value in cur_node.local_info.items()
                if prop_value is not None and (
                        not isinstance(prop_value, dict) or not isinstance(prop_value, list) or len(prop_value) > 0
                ) and prop_key not in {'type', 'content'}
            }
            current_level_rendered['type'] = cur_node.type
            if 'marks' in cur_node.local_info:
                current_level_rendered['marks'] = [child_node.render() for child_node in cur_node.local_info['marks']]
            if 'content' in cur_node.local_info:
                current_level_rendered['content'] = []
                render_queue.extend(
                    (child_node, current_level_rendered) for child_node in cur_node.local_info['content']
                )

            if parent_node is not None:
                parent_node['content'].append(current_level_rendered)
            else:
                top_node_rendered = current_level_rendered

        return top_node_rendered

    def assign_info(self, field, *values, **kwargs):
        """
        Assign value to field. Extend if the field is a list. Update if the field is a dict.
        :param field: Specified the field to be edited.
        :param values: Value to be added. List accepts multiple values.
        :param kwargs: Values to be added to a dict.
        :return: Current Node
        """
        if field not in self.local_info:
            raise KeyError(f'"{field}" does not exists in the node "{self.type}"')
        if field == 'content':
            raise ValueError(f'"{field}" is protected. Do not modify it with assign_info()')

        if isinstance(self.local_info[field], list):
            if len(values) == 0:
                raise RuntimeError("Field specified without specifying any value.")
            self.local_info[field].extend(list(values))

        elif isinstance(self.local_info[field], dict):
            if len(kwargs) > 0:
                self.local_info[field].update(kwargs)

        else:
            if len(values) != 1:
                raise RuntimeError(f'Specify 1 value for the field "{field}"')
            self.local_info[field] = values[0]

        return self

    def apply_variable(self, **kwargs):
        """
        Replace all format string expressions under this node, including all child nodes.
        This routine check all inputs to avoid code injection.
        :param kwargs: Variables to be replaced.
        :return: Current Node
        """
        resolve_queue = [self]
        while resolve_queue:
            cur_obj = resolve_queue.pop(0)
            if issubclass(type(cur_obj), ADFObject):
                cur_obj = cur_obj.local_info
            if isinstance(cur_obj, dict):
                for item_key, item_value in cur_obj.items():
                    if item_key in ('content', 'marks'):
                        resolve_queue.extend(item_value)
                    if isinstance(item_value, dict):
                        resolve_queue.append(item_value)
                    if isinstance(item_value, str) and (expressions := ADFObject.PATTERN_EXP.findall(item_value)):
                        invalid_variables = [expression for expression in expressions if
                                             ADFObject.PATTERN_VAR.fullmatch(expression[1:-1].strip()) is None]
                        if invalid_variables:
                            raise ValueError(f'Invalid expression detected: {invalid_variables}')
                        cur_obj[item_key] = item_value.format(**kwargs)

        return self


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


def load_adf(input_object: dict):
    if 'type' not in input_object:
        return ValueError('Loading ADF document with the filed "type" missing.')
    new_node = ADFDoc() if (input_type := input_object['type']) == 'doc' else ADFObject(input_type)

    for field, value in input_object.items():
        if field == 'type':
            continue
        if isinstance(value, dict):
            new_node.assign_info(field, **value)
        elif isinstance(value, list):
            if field == 'content':
                new_node.extend_content([load_adf(child_node) for child_node in value])
            if field == 'marks':
                new_node.assign_info(field, *[load_adf(child_node) for child_node in value])
        else:
            new_node.assign_info(field, value)

    return new_node
