from datetime import datetime

import pytest

from atlassian_doc_builder import ADFStrong, ADFEm, ADFStrike, ADFCode, ADFUnderline, ADFHardBreak, ADFRule
from atlassian_doc_builder import ADFText, ADFLink, ADFDate, ADFPlaceholder
from atlassian_doc_builder import load_adf


class TestADFSimpleObject:
    @pytest.mark.parametrize("node_class,node_type",
                             zip((
                                     ADFStrong, ADFEm, ADFStrike, ADFCode,
                                     ADFUnderline, ADFHardBreak, ADFRule,
                                     ADFDate, ADFPlaceholder,
                             ), (
                                     'strong', 'em', 'strike', 'code',
                                     'underline', 'hardBreak', 'rule',
                                     'date', 'placeholder',
                             )))
    def test_adf_simple_objects(self, node_type, node_class):
        assert node_class().type == node_type

    def test_adf_text(self):
        text = ADFText(text_content := 'foo bar')
        assert text.render()['text'] == text_content

    @pytest.mark.parametrize("node_class", (
            ADFText, ADFPlaceholder
    ))
    def test_adf_text_property(self, node_class):
        text = node_class(text_content := 'foo bar')
        assert text.text == text_content

    @pytest.mark.parametrize("node_class", (
            ADFText, ADFPlaceholder
    ))
    def test_adf_text_property_set(self, node_class):
        text_content = 'foo bar'
        text = node_class('dummy')
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
        assert float(date.timestamp) - t0 < 5  # sec

    def test_date_timestamp_in_sec(self):
        date = ADFDate(time_in_sec := 1676596381)
        assert date.timestamp == time_in_sec

    def test_date_timestamp_in_ms(self):
        date = ADFDate(time_in_ms := 1676596381123)
        assert date.timestamp == time_in_ms // 1000

    def test_date_timestamp_in_string(self):
        date = ADFDate(time_in_ms := (time_in_s := "1676596381") + "185")
        assert date.timestamp == int(time_in_s)
        date.render()['attrs']['timestamp'] == time_in_ms
