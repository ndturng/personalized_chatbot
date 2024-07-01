import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.query import query_similar_documents
from GPT_response import generate_response_from_results


def main():
    st.set_page_config(page_title="Chat with PDFs")
    st.header("Chat with PDFs")

    st.write(
        "The pdf file is a book called 'I, Steve: Steve Jobs in His Own Words'."
    )

    st.write("Ask something about Steve Jobs")

    st.write("You can ask questions like: What is Steve's favorite food?")

    # Initialize session state if it doesn't exist
    if 'response_text' not in st.session_state:
        st.session_state.response_text = ""
    if 'sources' not in st.session_state:
        st.session_state.sources = []
    
    query_text = st.text_input(
        label="Ask a question", placeholder="Type your question here"
    )
    
    if st.button("Submit Query"):
        if query_text:
            query_result = query_similar_documents(query_text, top_k=5)
            st.session_state.response_text, st.session_state.sources = generate_response_from_results(
                query_result, query_text
            )
    
    if st.session_state.response_text:
        st.write(f"Response: {st.session_state.response_text}")
        if st.button("Show Sources"):
            st.write("Sources:")
            for source in st.session_state.sources:
                st.write(source)
            


if __name__ == "__main__":
    main()
