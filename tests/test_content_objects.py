import pytest

from atlassian_doc_builder import ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem, ADFMediaGroup
from atlassian_doc_builder import ADFHeading, ADFCodeBlock, ADFPanel, ADFMediaSingle


class TestADFContentObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem,
                                     ADFMediaGroup
                             ), (
                                     'paragraph', 'blockquote',
                                     'bulletList', 'orderedList', 'listItem',
                                     'mediaGroup',
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

    def test_media_single(self):
        obj1 = ADFPanel(layout := "center")
        obj2 = ADFPanel(layout, width := 23.5)
        assert obj1.layout == layout
        assert obj2.layout == layout and obj2.width == width
        obj1.width, obj2.layout = width, "align-end"
        assert obj2.layout != layout and obj1.width == width
