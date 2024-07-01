import os
import sys
from pathlib import Path

import requests
from langchain_core.documents.base import Document

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pdf_process import process_pdf

from untils.constants import DATA_FOLDER, URL


# handle to create better schema
def create_schema(
    schema_name: str = "ExampleSchema",
    vectorizer: str = "text2vec-contextionary",
    moduleConfig: dict = {"text2vec-contextionary": {}},
):
    if check_schema(schema_name):  # handle to show schema exists
        print(f"Schema {schema_name} already exists.")
        return
    else:
        print(f"Creating schema {schema_name}...")
    schema_data = {
        "class": schema_name,
        "vectorizer": vectorizer,
        "moduleConfig": moduleConfig,
    }
    create_schema_response = requests.post(f"{URL}/schema", json=schema_data)
    if create_schema_response.status_code != 200:
        print(f"Failed to create schema. error: {create_schema_response.text}")
        print(
            f"Failed to create schema. Status code: {create_schema_response.status_code}"
        )
        sys.exit(1)
    else:
        print(f"Schema {schema_name} created successfully.")


def check_schema(schema_name=None):
    response = requests.get(f"{URL}/schema/{schema_name}")
    if response.status_code != 200:
        return False
    else:
        return True


def delete_schema(schema_name: str):
    if not check_schema(schema_name):  # check if the schema exists
        print(f"Schema {schema_name} does not exist.")
        return

    response = requests.delete(f"{URL}/schema/{schema_name}")
    if response.status_code != 200:
        print(f"Failed to delete schema. Error: {response.text}")
        print(f"Failed to delete schema. Status code: {response.status_code}")
        sys.exit(1)
    print(f"Schema {schema_name} deleted successfully.")


# upload data from folder
def upload_data(data_chunks: list[Document], schema_name: str):
    for chunk in data_chunks:
        properties = {
            "title": chunk.metadata["source"].split("/")[-1],
            "content": chunk.page_content,
            "source": chunk.metadata["source"]
            + " - "
            + "page:"
            + " "
            + str(chunk.metadata["page"]),
        }

        response = requests.post(
            f"{URL}/objects",
            json={"class": f"{schema_name}", "properties": properties},
        )

        if response.status_code != 200:
            print(f"Failed to upload data. error: {response.text}")
            print(f"Failed to upload data. Status code: {response.status_code}")
            sys.exit(1)
        print(f"Data in {properties['source']} uploaded successfully.")
    print(f"All of {len(data_chunks)} data chunks uploaded successfully.")


def delete_data(uuid=None):
    if uuid:
        response = requests.delete(f"{URL}/objects/{uuid}")
        if response.status_code not in [200, 204]:
            print(
                f"Failed to delete data with UUID {uuid}. error: {response.text}"
            )
            print(f"Failed to delete data. Status code: {response.status_code}")
            sys.exit(1)
        print(f"Data with UUID {uuid} deleted successfully.")
    else:
        while True:
            response = requests.get(f"{URL}/objects")
            # check if there are objects to delete
            if response.status_code != 200:
                print(f"Failed to retrieve objects. error: {response.text}")
                print(
                    f"Failed to retrieve objects. Status code: {response.status_code}"
                )
                sys.exit(1)

            objects = response.json().get("objects", [])

            if not objects:
                print("No more objects to delete.")
                break

            for obj in objects:
                obj_uuid = obj["id"]
                delete_response = requests.delete(f"{URL}/objects/{obj_uuid}")
                if delete_response.status_code not in [200, 204]:
                    print(
                        f"Failed to delete data with UUID {obj_uuid}. error: {delete_response.text}"
                    )
                    print(
                        f"Failed to delete data. Status code: {delete_response.status_code}"
                    )
                    sys.exit(1)
                print(f"Data with UUID {obj_uuid} deleted successfully.")


# Main script
if __name__ == "__main__":

    if len(sys.argv) < 2 or sys.argv[1] not in [
        "schema",
        "upload",
        "check",
        "delete",
        "all",
    ]:
        print("Usage: python script.py {schema|upload|check|delete|all} [uuid]")

        # for testing
        # print("No valid command provided, run the testing script...")
        # create_schema()
        # delete_schema("ExampleSchema")
        # if check_schema("ExampleSchema"):
        #     print("Schema exists")

        sys.exit(1)

    if sys.argv[1] == "schema":
        create_schema()
    elif sys.argv[1] == "upload":
        create_schema("ExampleSchema")
        data_chunks = process_pdf(DATA_FOLDER)
        upload_data(data_chunks, "ExampleSchema")
    elif sys.argv[1] == "delete":
        if len(sys.argv) == 3:
            delete_data(sys.argv[2])
        else:
            delete_data()
    elif sys.argv[1] == "all":
        create_schema()
        upload_data()
