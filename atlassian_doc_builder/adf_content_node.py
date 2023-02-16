from copy import deepcopy

import jsonschema

from .adf_object import ADFContentObject
from .adf_object import adf_schema

ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem, ADFMediaGroup = tuple(
    ADFContentObject.node_class_factory(node_type)
    for node_type in (
        'paragraph', 'blockquote',
        'bulletList', 'orderedList', 'listItem',
        'mediaGroup',
    )
)


class ADFDoc(ADFContentObject.node_class_factory('doc')):
    def __init__(self, chain_mode=True, **kwargs):
        super(ADFDoc, self).__init__(chain_mode=chain_mode, **kwargs)
        self.local_info['version'] = 1

    def validate(self):
        """
        Validate the output object with the ADF Schema. Raise Exception when validation fails.
        :return: Rendered result
        """
        render_result = self.render()
        jsonschema.validate(render_result, adf_schema())
        return render_result


class ADFHeading(ADFContentObject.node_class_factory('heading')):
    def __init__(self, level=None, chain_mode=True, **kwargs):
        new_attrs = {'level': level} \
            if level is not None else deepcopy(kwargs.get('attrs', {}))
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFHeading, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def level(self):
        return self.local_info['attrs']['level']

    @level.setter
    def level(self, value):
        self.local_info['attrs']['level'] = value


class ADFCodeBlock(ADFContentObject.node_class_factory('codeBlock')):
    def __init__(self, language=None, chain_mode=True, **kwargs):
        new_attrs = {'language': language} \
            if language is not None else deepcopy(kwargs.get('attrs', {}))
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFCodeBlock, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def language(self):
        return self.local_info['attrs']['language']

    @language.setter
    def language(self, value):
        self.local_info['attrs']['language'] = value


class ADFPanel(ADFContentObject.node_class_factory('panel')):
    def __init__(self, panel_type=None, chain_mode=True, **kwargs):
        new_attrs = {'panelType': panel_type} \
            if panel_type is not None else deepcopy(kwargs.get('attrs', {}))
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFPanel, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def panel_type(self):
        return self.local_info['attrs']['panelType']

    @panel_type.setter
    def panel_type(self, value):
        self.local_info['attrs']['panelType'] = value


class ADFMediaSingle(ADFContentObject.node_class_factory('mediaSingle')):
    def __init__(self, layout=None, width=None, chain_mode=True, **kwargs):
        new_attrs = deepcopy(kwargs.get('attrs', {}))
        if layout is not None:
            new_attrs['layout'] = layout
        if width is not None:
            new_attrs['width'] = width
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFMediaSingle, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def layout(self):
        return self.local_info['attrs']['layout']

    @layout.setter
    def layout(self, value):
        self.local_info['attrs']['layout'] = value

    @property
    def width(self):
        return self.local_info['attrs']['width']

    @width.setter
    def width(self, value):
        self.local_info['attrs']['width'] = value
