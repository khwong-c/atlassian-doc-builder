import json
from atlassian_doc_builder import load_adf, ADFDoc

if __name__ == '__main__':
    with open('input.json') as f:
        raw_input = json.load(f)
    content1_objs = load_adf(raw_input)
    for obj in content1_objs:
        obj.apply_variable(
            title="Hi World",
        )

    content2_objs = load_adf(raw_input)
    for obj in content2_objs:
        obj.apply_variable(
            title="Good-bye World",
        )
    doc = ADFDoc().extend_content(content1_objs).extend_content(content2_objs)
    rendered = doc.validate()
    print(json.dumps(rendered, indent=2))
