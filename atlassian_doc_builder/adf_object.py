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
    PATTERN_EXP, PATTERN_VAR = re.compile(r'\{[^}]+\}'), re.compile('[0-9a-zA-Z_]+')

    def __init__(self, node_type, chain_mode=True, **kwargs):
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
        self._node_prop = self._object_list[self.type]['prop']
        self.local_info = {
            prop_key: ADFObject._default_field(prop_type)
            for prop_key, prop_type in self._node_prop.items()
            if prop_key in self._object_list[self.type]['required']
        }
        if kwargs:
            for key, value in kwargs.items():
                self.assign_info(key, value)

    @property
    def parent(self):
        return self._parent

    def add(self, key_or_node, chain_mode=None, **kwargs):
        """
        Add a node to the current node.
        :param key_or_node: Key of the new node or existing node created.
        :param chain_mode: Chain Mode of the new node created by key. Existing node not affected.
        :param kwargs: Extra info to be assigned to the new node.
        :return: self.chain_mode ? Current node : New Node
        """
        new_chain_mode = self.chain_mode if chain_mode is None else chain_mode
        new_node = key_or_node if issubclass(type(key_or_node), ADFObject) else ADFObject(key_or_node,
                                                                                          chain_mode=new_chain_mode)
        new_node_field_name = 'marks' if new_node.is_mark else 'content'
        if new_node_field_name not in self._node_prop:
            raise ValueError(f'Adding a {new_node_field_name}: {new_node.type} to node: {self.type} is forbidden.')
        self.assign_info(new_node_field_name, new_node)

        for field, value in kwargs.items():
            new_node.assign_info(field, value)

        return self if self.chain_mode else new_node

    def extend_content(self, nodes):
        """
        Add a list of existing nodes to the current node. Marks are not allowed.
        :param nodes: List of input nodes
        :return: Current Node
        """
        nodes = [nodes] if not isinstance(nodes, list) else nodes
        return self.assign_info('content', *nodes)

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
        if field not in self._node_prop:
            raise KeyError(f'"{field}" does not exists in the node "{self.type}"')
        if field == 'content':
            if any(not issubclass(type(node), ADFObject) or not node.is_node for node in values):
                raise RuntimeError(f'"{field} only accepts ADFObject which is a node.')
        if field == 'marks':
            if any(not issubclass(type(node), ADFObject) or not node.is_mark for node in values):
                raise RuntimeError(f'"{field} only accepts ADFObject which is a mark.')
        self.local_info.setdefault(field, ADFObject._default_field(self._node_prop[field]))

        if isinstance(self.local_info[field], list):
            if field in ('content', 'marks'):
                for node in values:
                    node._parent = self
            if values:
                if isinstance(values[0], list):
                    self.local_info[field].extend(values[0])
                else:
                    self.local_info[field].extend(list(values))

        elif isinstance(self.local_info[field], dict):
            if kwargs:
                self.local_info[field].update(kwargs)
            elif values:
                self.local_info[field].update(values[0])

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

    @staticmethod
    def _default_field(prop_type):
        return {
            'array': list, 'object': dict,
            'string': str, 'enum': str,
            'number': int,
        }.get(prop_type, lambda: None)()


class ADFDoc(ADFObject):
    def __init__(self, chain_mode=True):
        super(ADFDoc, self).__init__('doc', chain_mode=chain_mode)
        self.local_info['version'] = 1

    def validate(self):
        """
        Validate the output object with the ADF Schema. Raise Exception when validation fails.
        :return: Rendered result
        """
        render_result = self.render()
        jsonschema.validate(render_result, adf_schema())
        return render_result


def load_adf(input_object: dict):
    if 'type' not in input_object:
        raise ValueError('Loading ADF document with the filed "type" missing.')
    top_node = None

    build_queue = [([input_object], None)]
    while build_queue:
        input_objects, parent_node = build_queue.pop(0)
        for input_object in input_objects:
            new_node = ADFDoc() if (input_type := input_object['type']) == 'doc' else ADFObject(input_type)

            for field, value in input_object.items():
                if field == 'type':
                    continue
                if field in ('content', 'marks'):
                    new_node.assign_info(field)
                    build_queue.append((value, new_node))
                    continue
                new_node.assign_info(field, value)

            if parent_node is not None:
                parent_node.add(new_node)
            else:
                top_node = new_node
    return top_node
