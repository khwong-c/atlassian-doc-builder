from .adf_object import ADFObject
from copy import deepcopy

# Node Type with no inputs
ADFStrong, ADFEm, ADFStrike, ADFCode, ADFUnderline, ADFHardBreak, ADFRule = tuple(
    ADFObject.node_class_factory(node_type)
    for node_type in (
        'strong', 'em', 'strike', 'code', 'underline',
        'hardBreak', 'rule',
    )
)


class ADFText(ADFObject.node_class_factory('text')):
    def __init__(self, text=None, chain_mode=True, **kwargs):
        if not text and 'text' not in kwargs:
            raise ValueError('Text cannot be empty.')
        super(ADFText, self).__init__(text=text, chain_mode=chain_mode, **kwargs)

    @property
    def text(self):
        return self.local_info['text']
    
    @text.setter
    def text(self, value):
        self.local_info['text'] = value


class ADFLink(ADFObject.node_class_factory('link')):
    def __init__(self, url=None, chain_mode=True, **kwargs):
        new_kwargs = deepcopy(kwargs)
        new_kwargs.setdefault('attrs', {})
        if url is not None:
            new_kwargs['attrs']['href'] = url
        super(ADFLink, self).__init__(chain_mode=chain_mode, **new_kwargs)

    @property
    def url(self):
        return self.local_info['attrs']['href']
    
    @url.setter
    def url(self, value):
        self.local_info['attrs']['href'] = value
