from copy import deepcopy
from datetime import datetime

from .adf_object import ADFObject

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


class ADFDate(ADFObject.node_class_factory('date')):
    def __init__(self, timestamp=None, chain_mode=True, **kwargs):
        new_attrs = {
            'timestamp': str(
                kwargs.get('attrs', {}).get('timestamp',
                                            (datetime.now().timestamp() if timestamp is None else timestamp) * 1000
                                            )
            )
        }
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFDate, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def timestamp(self):
        return self.local_info['attrs']['timestamp']

    @timestamp.setter
    def timestamp(self, value):
        self.local_info['attrs']['timestamp'] = value


class ADFPlaceholder(ADFObject.node_class_factory('placeholder')):
    def __init__(self, text=None, chain_mode=True, **kwargs):
        new_attrs = {'text': text} \
            if text is not None else deepcopy(kwargs.get('attrs', {}))
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFPlaceholder, self).__init__(chain_mode=chain_mode, attrs=new_attrs, **new_kwargs)

    @property
    def text(self):
        return self.local_info['attrs']['text']

    @text.setter
    def text(self, value):
        self.local_info['attrs']['text'] = value
