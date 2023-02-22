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
        self.assign_info('text', value)


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


class ADFDate(ADFObject.node_class_factory('date')):
    def __init__(self, timestamp=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFDate, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.timestamp = timestamp if timestamp is not None else \
            kwargs.get('attrs', {}).get('timestamp', (datetime.now().timestamp()))

    @property
    def timestamp(self):
        return int(self.local_info['attrs'].get('timestamp')) // 1000

    @timestamp.setter
    def timestamp(self, value):
        self.assign_info('attrs', timestamp=value if isinstance(value, str) else str(value * 1000))


class ADFPlaceholder(ADFObject.node_class_factory('placeholder')):
    def __init__(self, text=None, chain_mode=True, **kwargs):
        new_kwargs = {k: v for k, v in kwargs.items() if k != 'attrs'}
        super(ADFPlaceholder, self).__init__(chain_mode=chain_mode, **new_kwargs)
        self.text = text if text is not None else \
            kwargs.get('attrs', {}).get('text', '')

    @property
    def text(self):
        return self.local_info['attrs'].get('text')

    @text.setter
    def text(self, value):
        self.assign_info('attrs', text=value)
