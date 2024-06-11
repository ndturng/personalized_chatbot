import sys

import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.query import MetadataQuery
from weaviate.connect import ConnectionParams

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
            )
        )
    finally:
        client.close()

    print(f"Query text: {query}\n")
    print(f"Top {top_k} similar documents:")
    for obj in response.objects:
        
        # print(f"UUID: {obj.properties['uuid']}")
        print(f"Source: {obj.properties['source']}")
        print(f"Content: {obj.properties['content']}\n")
    
    return response.objects


# Main script
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python script.py query [top_k]")
    #     sys.exit(1)

    # query = sys.argv[1]
    
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    query_similar_documents(query_text, top_k)
