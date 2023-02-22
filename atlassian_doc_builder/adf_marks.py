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
            kwargs.get('attrs', {}).get('mode', '')

    @property
    def mode(self):
        return self.local_info['attrs'].get('mode')

    @mode.setter
    def mode(self, value):
        self.assign_info('attrs', mode=value)
