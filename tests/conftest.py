import pytest
import json
import yaml


@pytest.fixture
def reference_test_objects():
    with open('tests/test_cases.yaml') as f:
        return yaml.safe_load(f)
