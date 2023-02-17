# Atlassian Document Builder

Creating Atlassian Document in a programmatic way.

## Description

Provide an automatic way to generate documents and report on Atlassian Platform (e.g. Confluence, Jira).
Developer may automate report publication (e.g. functional verification report / requirement documents) into CI.

## Getting Started

### Dependencies

- Python3.8+

### Installing

```shell
pip install atlassian-doc-builder
```

## Features

- Tree-Like Document Representation
- JSON ADF Rendering and Parsing
- Reusable Template with variable filling 
- Document Validation

## Implemented Node Type

Please refer to [this document](Implemented_nodes.md).

## Roadmap

- [x] Create Base Class for ADF Object
- [x] Implement Basic Features above
- [x] Derive common classes for easy access (e.g. Text, Paragraph)
- [ ] Add short hands functions to create document
- [x] Table Editor and Table Row Editor
- [ ] Media Display

## Examples

Please refer to [the "examples" directory](examples).

## Version History

- 0.4
  - Implement Table Objects with creation routine
  - Implement set of Block Nodes with children
  - Index access to child nodes with `[]`. Multiple index supported. e.g. `doc[1,2,3]`
- 0.3
  - Support `ADFText`, `ADFLink` and a bunch of one line classes
  - ADFObject Class Factory for quick Class Development
- 0.2
  - Add Test Suite
  - Improve ADFObject Implementations
- 0.1
  - Initial Release

## Contribution and Contact

Pull Requests and Discussion are welcome on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

This Project is inspired by:
- [pyadf project from Atlassian](https://bitbucket.org/atlassian/pyadf)
