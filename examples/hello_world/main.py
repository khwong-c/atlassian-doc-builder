import json

from atlassian_doc_builder import ADFObject, ADFDoc, ADFText, ADFLink

if __name__ == '__main__':
    doc = ADFDoc()
    doc.add(
        h1 := ADFObject('heading', attrs={'level': 1})
    ).add(
        h2 := ADFObject('heading', attrs={'level': 2})
    )
    h1.add(ADFText('Hello World'))
    h2.add(
        ADFText('Get me to the Repo').add('em').add(ADFLink('https://github.com/khwong-c/atlassian-doc-builder'))
    )
    rendered = doc.validate()
    print(json.dumps(rendered, indent=2))
