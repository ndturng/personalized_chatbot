from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from data.query import query_similar_documents

# Get OpenAI API key from the .env file
load_dotenv()


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def generate_response_from_results(query_result, query_text):
    if query_result is None:
        return None, None

    # Preparing the context text from the search results
    context_text = "\n\n---\n\n".join(
        [obj.properties["content"] for obj in query_result]
    )

    # Using a template for generating the prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Printing the prompt for debugging or logging
    print(prompt)

    # Generate the response using the model
    model = ChatOpenAI()
    response_text = model.invoke(prompt).content

    # Preparing the source information
    sources = []
    for obj in query_result:
        source = obj.properties["source"]
        content = obj.properties["content"]

        source_info = f">File: {source} - \
            Source: {content}\
            \n>>> {content}\n\n"

        sources.append(source_info)

    return response_text, sources


def main():
    query_text = "What about the customer service?"
    query_result = query_similar_documents(query_text, 5)

    response_text, sources = generate_response_from_results(
        query_result, query_text
    )
    print(f"Response: {response_text}\n")


if __name__ == "__main__":
    main()
