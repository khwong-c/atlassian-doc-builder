import pytest

from atlassian_doc_builder import ADFDoc, ADFObject, load_adf
from .utils import render_output_text


class TestADFObject:
    def test_chain_add(self):
        result = ADFDoc().add('paragraph').add('paragraph').add('paragraph').validate()
        assert len(result['content']) == 3, f"3 content nodes expected, {len(result['content'])} found instead."

    def test_chain_mode_false(self, reference_test_objects):
        result = ADFDoc(chain_mode=False) \
            .add('paragraph') \
            .add('text').assign_info('text', 'foo').parent \
            .add('text').assign_info('text', 'bar').parent.parent \
            .validate()
        assert render_output_text(result) == render_output_text(reference_test_objects['test_chain_mode_false'])

    def test_add_node_with_arguments(self, reference_test_objects):
        paragraph = ADFObject('paragraph')
        paragraph.add('text', text='foo').add('text', text='bar')
        assert render_output_text(paragraph) == render_output_text(reference_test_objects['test_apply_var_out'])

    def test_apply_variable_success(self, reference_test_objects):
        template = load_adf(reference_test_objects['test_apply_var_in'])
        template.apply_variable(text_a='foo', text_b='bar')
        assert render_output_text(template) == render_output_text(reference_test_objects['test_apply_var_out'])

    @pytest.mark.parametrize("test_case", [
        "test_apply_var_assignment",
        "test_apply_var_function",
        "test_apply_var_member",
        "test_apply_var_array",
        "test_apply_var_dict",
    ])
    def test_apply_variable_forbidden(self, reference_test_objects, test_case):
        with pytest.raises(ValueError):
            template = load_adf(reference_test_objects[test_case])
            template.apply_variable()

    def test_track_parent_add(self):
        doc = ADFDoc(chain_mode=False)
        assert doc.add('paragraph').add('text').add('strong') \
                   .parent.parent.parent == doc

    def test_track_parent_extend(self):
        doc = ADFDoc(chain_mode=False)
        paragraph = ADFObject('paragraph')
        doc.extend_content(paragraph)
        assert paragraph.parent == doc

    def test_track_parent_assign_info(self):
        doc = ADFDoc(chain_mode=False)
        paragraph = ADFObject('paragraph')
        strong = ADFObject('strong')
        doc.assign_info('content', paragraph)
        paragraph.assign_info('marks', strong)
        assert strong.parent.parent == doc


class TestADFObjectCoverage:
    def test_load_malformed_object(self):
        with pytest.raises(ValueError):
            load_adf({'content': []})

    def test_create_non_exists_adf_object(self):
        with pytest.raises(RuntimeError):
            ADFObject('foo')
