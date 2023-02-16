import json
from atlassian_doc_builder import load_adf

if __name__ == '__main__':
    with open('input.json') as f:
        raw_input = json.load(f)
    doc = load_adf(raw_input)
    rendered = doc.validate()
    print(json.dumps(rendered, indent=2))
