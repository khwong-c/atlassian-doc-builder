import jsonschema

from .adf_object import adf_schema, ADFObject


class ADFContentObject(ADFObject):
    def __getitem__(self, idx):
        if type(idx) is int:
            return self.local_info['content'][idx]
        levels, cur_obj = list(idx), self.local_info['content']
        while levels:
            cur_idx = levels.pop(0)
            cur_obj = cur_obj[cur_idx]
            if not levels:
                return cur_obj
            cur_obj = cur_obj.local_info['content']

    def __len__(self):
        return len(self.local_info['content'])

    def __iter__(self):
        return self.local_info['content'].__iter__()


ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem = tuple(
    ADFContentObject.node_class_factory(node_type)
    for node_type in (
        'paragraph', 'blockquote',
        'bulletList', 'orderedList', 'listItem',
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
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFHeading, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.level = level if level is not None else \
            kwargs.get('attrs', {}).get('level', 1)

    @property
    def level(self):
        return self.local_info['attrs']['level']

    @level.setter
    def level(self, value):
        self.assign_info('attrs', level=value)


class ADFCodeBlock(ADFContentObject.node_class_factory('codeBlock')):
    def __init__(self, language=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFCodeBlock, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.language = language if language is not None else \
            kwargs.get('attrs', {}).get('language', '')

    @property
    def language(self):
        return self.local_info['attrs'].get('language')

    @language.setter
    def language(self, value):
        self.assign_info('attrs', language=value)


class ADFPanel(ADFContentObject.node_class_factory('panel')):
    def __init__(self, panel_type=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        new_attrs = {k: v for k, v in kwargs.get('attrs', {}).items() if k != 'panelType'}
        super(ADFPanel, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)
        self.panel_type = panel_type if panel_type is not None else \
            kwargs.get('attrs', {}).get('panelType', 'info')

    @property
    def panel_type(self):
        return self.local_info['attrs'].get('panelType')

    @panel_type.setter
    def panel_type(self, value):
        self.assign_info('attrs', panelType=value)


class ADFExpand(ADFContentObject.node_class_factory('expand')):
    def __init__(self, title=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFExpand, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.title = title if title is not None else \
            kwargs.get('attrs', {}).get('title', '')

    @property
    def title(self):
        return self.local_info['attrs'].get('title')

    @title.setter
    def title(self, value):
        self.assign_info('attrs', title=value)


class ADFTaskList(ADFContentObject.node_class_factory('taskList')):
    def __init__(self, local_id=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFTaskList, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.local_id = local_id if local_id is not None else \
            kwargs.get('attrs', {}).get('localId', '')

    @property
    def local_id(self):
        return self.local_info['attrs'].get('localId')

    @local_id.setter
    def local_id(self, value):
        self.assign_info('attrs', localId=value)


class ADFTaskItem(ADFContentObject.node_class_factory('taskItem')):
    def __init__(self, state=None, local_id=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFTaskItem, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.state = state if state is not None else \
            kwargs.get('attrs', {}).get('state', '')
        self.local_id = local_id if local_id is not None else \
            kwargs.get('attrs', {}).get('localId', '')

    @property
    def state(self):
        return self.local_info['attrs'].get('state')

    @state.setter
    def state(self, value):
        self.assign_info('attrs', state=value)

    @property
    def local_id(self):
        return self.local_info['attrs'].get('localId')

    @local_id.setter
    def local_id(self, value):
        self.assign_info('attrs', localId=value)
