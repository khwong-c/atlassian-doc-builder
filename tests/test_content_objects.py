import pytest

from atlassian_doc_builder import ADFHeading, ADFCodeBlock, ADFPanel
from atlassian_doc_builder import ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem
from atlassian_doc_builder import ADFText


class TestADFContentObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem,
                             ), (
                                     'paragraph', 'blockquote',
                                     'bulletList', 'orderedList', 'listItem',
                             )))
    def test_content_objects(self, node_type, node_class):
        assert node_class().type == node_type

    def test_heading(self):
        obj = ADFHeading(level := 2)
        assert obj.level == level
        obj.level = (new_level := 3)
        assert obj.level == new_level

    def test_code_block(self):
        obj = ADFCodeBlock(language := 'python')
        assert obj.language == language
        obj.language = (new_language := 'c++')
        assert obj.language == new_language

    def test_panel(self):
        obj = ADFPanel(panel_type := 'success')
        assert obj.panel_type == panel_type
        obj.panel_type = (new_type := 'error')
        assert obj.panel_type == new_type

    @pytest.mark.parametrize("node_class,addition_args",
                             zip((
                                     ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem,
                                     ADFHeading, ADFHeading, ADFHeading,
                                     ADFCodeBlock, ADFCodeBlock, ADFCodeBlock,
                                     ADFPanel, ADFPanel, ADFPanel,
                             ), (
                                     {}, {}, {}, {}, {},
                                     {}, {'level': 2}, {'attrs': {'level': 2}},
                                     {}, {'language': 'python'}, {'attrs': {'language': 'python'}},
                                     {}, {'panel_type': 'success'}, {'attrs': {'panelType': 'success'}},

                             )))
    def test_content_add_in_arguments(self, node_class, addition_args):
        obj = node_class(content=ADFText(new_text := 'foo'), **addition_args)
        assert obj[0].text == new_text
        if 'attrs' in addition_args:
            assert obj.local_info['attrs'] == addition_args['attrs']
        else:
            for k, v in addition_args.items():
                assert getattr(obj, k) == v
