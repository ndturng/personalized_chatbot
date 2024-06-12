import requests

from data.weaviate_init import create_schema, delete_schema

URL = "http://localhost:8080/v1"


def test_create_delete_schema():
    """
    Test create_schema function
    run these command before running the test:
    - make run

    """
    schema_name = "ExampleSchema"
    create_schema(schema_name)
    # schema ExampleSchema should be exit at URL/schema/ExampleSchema
    response = requests.get(f"{URL}/schema/{schema_name}")
    assert response.status_code == 200
    
    # delete schema ExampleSchema
    delete_schema(schema_name)
    response = requests.get(f"{URL}/schema/{schema_name}")
    assert response.status_code == 404
