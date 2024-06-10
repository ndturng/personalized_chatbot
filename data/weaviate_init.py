import json
import sys
from pathlib import Path

import requests
from pdf_process import process_pdf

DATA_FOLDER = "data/storage"
URL = "http://localhost:8080/v1"

sample_data = [
    {
        "uuid": "e3b1f1b3-7b3b-4b1f-8e8f-3f1b3b7b3b1f",
        "title": "The Power of Vector Search",
        "content": "Vector search engines revolutionize how we store and retrieve information. Unlike traditional search methods that rely on keyword matching, vector search utilizes mathematical representations (vectors) to understand the context and relationships between words, documents, and queries. This approach enables more accurate and contextually relevant search results, making it ideal for applications like natural language processing, recommendation systems, and semantic search.",
        "permissionLevel": 0,
        "source": "sample_file.pdf",
        "publishDate": "2023-05-15",
        "authorisedDepartments": ["all"],
    }
]


# handle to create better schema
def create_schema():
    if check_schema("Document"):  # handle to show schema exists
        print("Schema Document exists")
        return
    schema_data = {
        "class": "Document",
        "vectorizer": "text2vec-contextionary",
        "moduleConfig": {"text2vec-contextionary": {}},
    }
    response = requests.post(f"{URL}/schema", json=schema_data)
    if response.status_code != 200:
        print(f"Failed to create schema. error: {response.text}")
        print(f"Failed to create schema. Status code: {response.status_code}")
        sys.exit(1)
    print(response.text)


def check_schema(schema_name=None):
    response = requests.get(f"{URL}/schema/{schema_name}")
    if response.status_code != 200:
        print(f"Failed to get schema. error: {response.text}")
        print(f"Failed to get schema. Status code: {response.status_code}")
        return False
    else:
        return True


# upload data from folder
def upload_data(data_chunk: list):
    for item in data_chunk:
        properties = {
            "title": item.metadata["source"].split("/")[-1],
            "content": item.page_content,
            "source": item.metadata["source"]
            + " - "
            + "page:"
            + " "
            + str(item.metadata["page"]),
        }

        response = requests.post(
            f"{URL}/objects",
            json={"class": "Document", "properties": properties},
        )

        if response.status_code != 200:
            print(f"Failed to upload data. error: {response.text}")
            print(f"Failed to upload data. Status code: {response.status_code}")
            sys.exit(1)
        print(f"Data in {properties['source']} uploaded successfully.")
    print(f"All of {len(data_chunk)} data chunks uploaded successfully.")


# upload data from json file
def upload_data_from_json(file_path: Path):
    with open(file_path, "r") as file:
        data = json.load(file)
    for item in data:
        response = requests.post(
            f"{URL}/objects", json={"class": "Document", "properties": item}
        )
        if response.status_code != 200:
            print(f"Failed to upload data. error: {response.text}")
            print(f"Failed to upload data. Status code: {response.status_code}")
            sys.exit(1)
        print(f"Data with UUID {item['uuid']} uploaded successfully.")


def check_data():
    print("Checking data...")
    response = requests.get(f"{URL}/objects")

    if response.status_code != 200:
        print(f"Failed to retrieve objects. error: {response.text}")
        print(
            f"Failed to retrieve objects. Status code: {response.status_code}"
        )
        sys.exit(1)

    objects = response.json().get("objects", [])
    for obj in objects:
        obj_uuid = obj["properties"]["uuid"]
        print(f"Data with UUID {obj_uuid} exists.")


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

        # data_path = Path("data/fake_data.json")
        # upload_data_from_json(data_path)

        sys.exit(1)

    if sys.argv[1] == "schema":
        create_schema()
    elif sys.argv[1] == "upload":
        create_schema()
        data_chunks = process_pdf(DATA_FOLDER)
        upload_data(data_chunks)
    elif sys.argv[1] == "check":
        check_data()
    elif sys.argv[1] == "delete":
        if len(sys.argv) == 3:
            delete_data(sys.argv[2])
        else:
            delete_data()
    elif sys.argv[1] == "all":
        create_schema()
        upload_data()
        check_data()
