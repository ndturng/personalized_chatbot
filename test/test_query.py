import subprocess
from data.pdf_process import process_pdf
from data.query import query_similar_documents
from data.weaviate_init import create_schema, delete_schema, upload_data


def test_query():
    """
    - Run the tests of create_schema, delete_schema, and upload_data before running this test.
    - Run the command below to start the server before running the test:
        + make run
    """
    # start the server
    subprocess.run(["make", "run"])

    data_folder = "data/storage"
    schema_name = "ExampleSchema"
    # load and process the pdf files
    text_chunks = process_pdf(data_folder)

    # create the example schema
    create_schema(schema_name)
    # upload data to the server
    upload_data(text_chunks, schema_name)

    # query from the server
    query_text = "What about the customer service?"
    result = query_similar_documents(query_text, top_k=5)
    # delete the schema
    delete_schema(schema_name)
    assert len(result) == 5