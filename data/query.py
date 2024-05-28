import sys

import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.connect import ConnectionParams

# Constants
URL = "http://localhost:8080"

# Sample query text
query_text = "Explain the benefits of vector search engines."


def query_similar_documents(query, top_k=5):
    client = weaviate.WeaviateClient(
        connection_params=ConnectionParams.from_params(
            http_host="localhost",
            http_port="8080",
            http_secure=False,
            grpc_host="localhost",
            grpc_port="50051",
            grpc_secure=False,
        ),
        additional_config=AdditionalConfig(
            timeout=Timeout(init=2, query=45, insert=120),  # Values in seconds
        ),
    )

    client.connect()

    try:
        publications = client.collections.get("Document")
        response = publications.query.near_text(
            query=query,
            limit=top_k,
        )
    finally:
        client.close()

    for obj in response.objects:
        print(f"UUID: {obj.properties['uuid']}")
        print(f"Title: {obj.properties['title']}")
        print(f"Content: {obj.properties['content']}\n")


# Main script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py query [top_k]")
        sys.exit(1)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    query_similar_documents(query, top_k)
