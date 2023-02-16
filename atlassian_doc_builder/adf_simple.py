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


class ADFLink(ADFObject.node_class_factory('link')):
    def __init__(self, url=None, chain_mode=True, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs']['href'] = '' if url is None else url
        super(ADFLink, self).__init__(chain_mode=chain_mode, **kwargs)
