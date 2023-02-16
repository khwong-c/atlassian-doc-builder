import pytest

from atlassian_doc_builder import ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem
from atlassian_doc_builder import ADFHeading, ADFCodeBlock, ADFPanel

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

    @pytest.mark.parametrize("node_class",
                             (
                                     ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem,
                                     ADFHeading, ADFCodeBlock, ADFPanel,
                             ))
    def test_content_add_in_arguments(self, node_class):
        obj = node_class(content=ADFText(new_text := 'foo'))
        assert obj[0].text == new_text
