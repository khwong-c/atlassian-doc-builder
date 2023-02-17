import pytest

from atlassian_doc_builder import load_adf
from atlassian_doc_builder import ADFStrong, ADFEm, ADFStrike, ADFCode, ADFUnderline, ADFHardBreak, ADFRule
from atlassian_doc_builder import ADFText, ADFLink, ADFDate

from datetime import datetime

class TestADFSimpleObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFStrong, ADFEm, ADFStrike, ADFCode,
                                     ADFUnderline, ADFHardBreak, ADFRule
                             ), (
                                     'strong', 'em', 'strike', 'code',
                                     'underline', 'hardBreak', 'rule'
                             )))
    def test_adf_simple_objects(self, node_type, node_class):
        assert node_class().type == node_type

    def test_adf_text(self):
        text = ADFText(text_content := 'foo bar')
        assert text.render()['text'] == text_content

    def test_adf_text_property(self):
        text = ADFText(text_content := 'foo bar')
        assert text.text == text_content

    def test_adf_text_property_set(self):
        text_content = 'foo bar'
        text = ADFText('dummy')
        text.text = text_content
        assert text.text == text_content

    def test_adf_link(self):
        link = ADFLink(new_url := "http://localhost")
        assert link.render()['attrs']['href'] == new_url

    def test_adf_link_from_load_adf(self, reference_test_objects):
        link = load_adf(reference_test_objects['test_smoke_link'])
        assert 'http' in link.render()['attrs']['href']

    def test_adf_link_property(self):
        link = ADFLink(new_url := "http://localhost")
        assert link.url == new_url

    def test_adf_link_property_set(self):
        new_url = "http://docker_host"
        link = ADFLink("http://localhost")
        link.url = new_url
        assert link.url == new_url

    def test_date_empty(self):
        t0 = datetime.now().timestamp()
        date = ADFDate()
        assert float(date.timestamp) - t0 * 1000 < 5 * 1000  # ms

    def test_date_timestamp_in_sec(self):
        date = ADFDate(time_in_sec := 1676596381)
        assert date.timestamp == str(time_in_sec * 1000)
