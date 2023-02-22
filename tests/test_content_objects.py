import pytest

from atlassian_doc_builder import ADFHeading, ADFCodeBlock, ADFPanel
from atlassian_doc_builder import ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem, ADFExpand
from atlassian_doc_builder import ADFText
from atlassian_doc_builder import ADFTaskList, ADFTaskItem
from atlassian_doc_builder import ADFDecisionList, ADFDecisionItem


class TestADFContentObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFParagraph, ADFBlockquote, ADFBulletList, ADFOrderList, ADFListItem,
                                     ADFExpand
                             ), (
                                     'paragraph', 'blockquote', 'bulletList', 'orderedList', 'listItem',
                                     'expand',
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
                                     ADFExpand, ADFExpand, ADFExpand,
                                     ADFTaskList, ADFTaskList, ADFTaskList,
                                     ADFTaskItem, ADFTaskItem, ADFTaskItem,
                                     ADFTaskItem,
                                     ADFTaskItem,
                                     ADFTaskItem,
                                     ADFTaskItem,
                                     ADFDecisionList, ADFDecisionList, ADFDecisionList,
                                     ADFDecisionItem, ADFDecisionItem, ADFDecisionItem,
                                     ADFDecisionItem,
                                     ADFDecisionItem,
                                     ADFDecisionItem,
                                     ADFDecisionItem,
                             ), (
                                     {}, {}, {}, {}, {},
                                     {}, {'level': 2}, {'attrs': {'level': 2}},
                                     {}, {'language': 'python'}, {'attrs': {'language': 'python'}},
                                     {}, {'panel_type': 'success'}, {'attrs': {'panelType': 'success'}},
                                     {}, {'title': 'foo'}, {'attrs': {'title': 'foo'}},
                                     {}, {'local_id': 'foo'}, {'attrs': {'localId': 'foo'}},
                                     {}, {'local_id': 'foo'}, {'attrs': {'localId': 'foo'}},
                                     {'state': 'TODO', 'local_id': 'foo'},
                                     {'attrs': {'state': 'TODO', 'localId': 'foo'}},
                                     {'local_id': 'foo', 'attrs': {'state': 'TODO'}},
                                     {'state': 'TODO', 'attrs': {'localId': 'foo'}},
                             )))
    def test_content_add_in_arguments(self, node_class, addition_args):
        obj = node_class(content=ADFText(new_text := 'foo'), **addition_args)
        assert obj[0].text == new_text

        if 'attrs' in addition_args:
            rendered = obj.render()
            for k in addition_args['attrs']:
                assert rendered['attrs'][k] == addition_args['attrs'][k]
        else:
            for k, v in addition_args.items():
                assert getattr(obj, k) == v
