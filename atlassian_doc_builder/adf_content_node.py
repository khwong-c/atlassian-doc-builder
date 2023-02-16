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
