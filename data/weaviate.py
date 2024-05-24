import sys

import requests

URL = "http://localhost:8080/v1"


def create_schema():
    if check_schema("Document"):
        print("Schema already exists")
        sys.exit(0)
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


# Main script
if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["schema", "upload", "all"]:
        print("Usage: python script.py {schema|upload|all}")
        sys.exit(1)

    if sys.argv[1] == "schema":
        create_schema()
