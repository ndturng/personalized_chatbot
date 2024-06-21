import subprocess

import requests
from langchain_core.documents.base import Document

from data.weaviate_init import create_schema, delete_schema, upload_data
from untils.constants import URL
from untils.untils import wait_for_server


def test_create_delete_schema():
    """
    Test create_schema function and delete_schema function
    """
    # start the server
    subprocess.run(["make", "run"])
    # wait for the server to start
    wait_for_server(URL)

    schema_name = "ExampleSchema"
    create_schema(schema_name)
    # schema ExampleSchema should be exit at URL/schema/ExampleSchema
    response = requests.get(f"{URL}/schema/{schema_name}")
    assert response.status_code == 200

    # delete schema ExampleSchema
    delete_schema(schema_name)
    response = requests.get(f"{URL}/schema/{schema_name}")
    assert response.status_code == 404

    # stop the server
    subprocess.run(["make", "stop"])


def test_upload_data():
    """
    Test upload_data function
    """
    # start the server
    subprocess.run(["make", "run"])

    # wait for the server to start
    wait_for_server(URL)

    sample_data = [
        Document(
            page_content="This is a sample text",
            metadata={"source": "sample/source.pdf", "page": 0},
        )
    ]
    schema_name = "ExampleSchema"

    create_schema(schema_name)
    upload_data(sample_data, schema_name)
    # check if the data is uploaded successfully
    response = requests.get(f"{URL}/objects")
    assert response.status_code == 200

    # delete ExampleSchema schema, it will delete all the data in the schema
    delete_schema("ExampleSchema")
    response = requests.get(f"{URL}/schema/ExampleSchema")
    assert response.status_code == 404

    # stop the server
    subprocess.run(["make", "stop"])
