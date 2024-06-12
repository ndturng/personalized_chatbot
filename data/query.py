import logging
import sys

import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.query import MetadataQuery
from weaviate.connect import ConnectionParams

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
# Constants
URL = "http://localhost:8080"

# Sample query text
query_text = "What about the customer service?"


def query_similar_documents(query, top_k=5):
    client = weaviate.WeaviateClient(
        connection_params=ConnectionParams.from_params(
            http_host="localhost",
            http_port="8080",
            http_secure=False,
            grpc_host="localhost",  # A mine
            grpc_port="50051",
            grpc_secure=False,
        ),
        additional_config=AdditionalConfig(
            timeout=Timeout(init=2, query=45, insert=120),  # Values in seconds
        ),
    )
    # Try to connect to the client, if it fails, close the client and raise the exception
    try:
        client.connect()

    except Exception:
        logger.error("Failed to connect to the Weaviate client", exc_info=False)
        return None  # Optionally return an empty list or handle as needed

    try:
        publications = client.collections.get("Document")
        response = publications.query.hybrid(  # Based on the usecase, consider using hybrid or near_text
            query=query,
            limit=top_k,
            return_metadata=MetadataQuery(
                certainty=True,
                distance=True,
                # explain_score=True,
                # is_consistent=True,
                # rerank=True, this require to add a module
                score=True,
            ),
        )

    except Exception as e:
        logger.error(
            "Query failed", exc_info=False
        )  # exc_info=True for debugging
        raise e

    finally:
        client.close()

    return response.objects


# Main script
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python script.py query [top_k]")
    #     sys.exit(1)

    # query = sys.argv[1]

    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    results = query_similar_documents(query_text, top_k)

    if results is None:
        print("No results found.")
        sys.exit(1)  # Why used sys.exit(1) here?

    print(f"Query text: {query_text}\n")
    print(f"Top {top_k} similar documents:")
    for obj in results:
        print(f"Source: {obj.properties['source']}")
        print(f"Content: {obj.properties['content']}\n")
