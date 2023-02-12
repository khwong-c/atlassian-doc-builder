import json
from typing import Union

from atlassian_doc_builder import ADFObject


def render_output_text(input_object: Union[ADFObject, dict]):
    return json.dumps(input_object if type(input_object) is dict else input_object.render(), sort_keys=True)
