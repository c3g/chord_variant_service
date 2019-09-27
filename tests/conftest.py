import json
import pytest
import requests

from chord_variant_service.app import application


@pytest.fixture
def client():
    application.config["TESTING"] = True
    client = application.test_client()
    yield client


@pytest.fixture(scope="module")
def json_schema():
    r = requests.get("http://json-schema.org/draft-07/schema#")
    schema = json.loads(r.content)
    print(schema)
    yield schema