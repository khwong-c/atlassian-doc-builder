from .adf_object import ADFObject

# Node Type with no inputs
ADFStrong, ADFEm, ADFStrike, ADFCode, ADFUnderline = tuple(
    ADFObject.node_class_factory(node_type)
    for node_type in (
        'strong', 'em', 'strike', 'code', 'underline',
    )
)


class ADFLink(ADFObject.node_class_factory('link')):
    def __init__(self, url=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        new_attrs = {k: v for k, v in kwargs.get('attrs', {}).items() if k != 'href'}
        super(ADFLink, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)
        self.url = url if url is not None else \
            kwargs.get('attrs', {}).get('href', '#')

    @property
    def url(self):
        return self.local_info['attrs'].get('href')

    @url.setter
    def url(self, value):
        self.assign_info('attrs', href=value)


class ADFBreakout(ADFObject.node_class_factory('breakout')):
    def __init__(self, mode=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFBreakout, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.mode = mode if mode is not None else \
            kwargs.get('attrs', {}).get('mode', 'wide')

    @property
    def mode(self):
        return self.local_info['attrs'].get('mode')

    @mode.setter
    def mode(self, value):
        self.assign_info('attrs', mode=value)


class ADFSubsup(ADFObject.node_class_factory('subsup')):
    def __init__(self, type=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFSubsup, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.type = type if type is not None else \
            kwargs.get('attrs', {}).get('type', 'sub')

    @property
    def type(self):
        return self.local_info['attrs'].get('type')

    @type.setter
    def type(self, value):
        self.assign_info('attrs', type=value)


class ADFTextColor(ADFObject.node_class_factory('textColor')):
    def __init__(self, color=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFTextColor, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.color = color if color is not None else \
            kwargs.get('attrs', {}).get('color', '#000000')

    @property
    def color(self):
        return self.local_info['attrs'].get('color')

    @color.setter
    def color(self, value):
        self.assign_info('attrs', color=value)


class ADFAlignment(ADFObject.node_class_factory('alignment')):
    def __init__(self, align=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFAlignment, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.align = align if align is not None else \
            kwargs.get('attrs', {}).get('align', 'center')

    @property
    def align(self):
        return self.local_info['attrs'].get('align')

    @align.setter
    def align(self, value):
        self.assign_info('attrs', align=value)


class ADFIndentation(ADFObject.node_class_factory('indentation')):
    def __init__(self, level=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFIndentation, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.level = level if level is not None else \
            kwargs.get('level', {}).get('level', 1)

    @property
    def level(self):
        return self.local_info['attrs'].get('level')

    @level.setter
    def level(self, value):
        self.assign_info('attrs', level=value)
