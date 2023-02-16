import pytest

from atlassian_doc_builder import ADFStrong, ADFEm, ADFStrike, ADFCode, ADFUnderline, ADFHardBreak, ADFRule
from atlassian_doc_builder import ADFText, ADFLink


class TestADFSimpleObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFStrong, ADFEm, ADFStrike, ADFCode,
                                     ADFUnderline, ADFHardBreak, ADFRule
                             ), (
                                     'strong', 'em', 'strike', 'code',
                                     'underline', 'hardBreak', 'rule'
                             )))
    def test_adf_link(self, node_type, node_class):
        assert node_class().type == node_type

    def test_adf_text(self):
        text = ADFText(text_content := 'foo bar')
        assert text.render()['text'] == text_content

    def test_adf_link(self):
        link = ADFLink(new_url := "http://localhost")
        assert link.render()['attrs']['href'] == new_url
