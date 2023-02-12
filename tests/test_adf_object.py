import pytest

from atlassian_doc_builder import ADFDoc, ADFObject, load_adf, adf_node_list, adf_mark_list
from .utils import render_output_text


class TestSmoke:
    def test_node_list(self):
        assert type(adf_node_list()) is dict
        assert len(adf_node_list()) > 0

    def test_mark_list(self):
        assert type(adf_mark_list()) is dict
        assert len(adf_mark_list()) > 0

    def test_doc_rendering(self, reference_test_objects):
        result = ADFDoc()
        result.validate()
        assert render_output_text(result) == render_output_text(reference_test_objects['test_smoke_doc'])

    def test_doc_loading(self, reference_test_objects):
        input_object = reference_test_objects['test_smoke_doc']
        result = load_adf(input_object)
        result.validate()
        assert render_output_text(result) == render_output_text(input_object)

    @pytest.mark.parametrize(
        "test_input,expected_object_type",
        [("test_smoke_doc", ADFDoc), ("test_smoke_paragraph", ADFObject), ]
    )
    def test_doc_load_correct_type(self, reference_test_objects, test_input, expected_object_type):
        result = load_adf(reference_test_objects[test_input])
        assert type(result) is expected_object_type


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
