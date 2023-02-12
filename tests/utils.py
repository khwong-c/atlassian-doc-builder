import json
from atlassian_doc_builder import ADFObject


def render_output_text(input_object: ADFObject):
    return json.dumps(input_object.render(), sort_keys=True)