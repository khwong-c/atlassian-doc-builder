import pytest
import json
import yaml


@pytest.fixture
def reference_test_objects():
    with open('tests/test_cases.yaml') as f:
        return yaml.safe_load(f)


@pytest.fixture
def reference_test_output():
    with open('tests/test_cases.yaml') as f:
        testcases = yaml.safe_load(f)
    return {
        k: json.dumps(v, sort_keys=True)
        for k, v in testcases.items()
    }
