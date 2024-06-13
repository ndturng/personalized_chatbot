from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
# Data folder
data_folder = "data/storage"


def load_pdf_from_path(path: str) -> list:
    """
    Load all pdf documents from a given path.
    """
    print(f"Loading PDF documents from {path}")
    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()

    return docs


def slpit_text(docs: list) -> list[Document]:
    """
    Split the text into text chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # this based on how the real data looks like
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        separators=[
            "\n\n",  # Paragraph break
            ". ",  # Sentence end
            ", ",  # Comma with space
            "\n",  # Line break
            " ",  # Space
            ".",  # Period
            ",",  # Comma
            "\u200B",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
        ],
    )

    text_chunks = text_splitter.split_documents(docs)
    print(
        f"Split {len(docs)} pages of documents into {len(text_chunks)} chunks."
    )
    return text_chunks


def process_pdf(data_folder: str) -> list:
    """
    Process the pdf files in the given folder.
    """
    docs = load_pdf_from_path(data_folder)
    text_chunks = slpit_text(docs)
    return text_chunks


if __name__ == "__main__":
    text_chunks = process_pdf(data_folder)
    print(text_chunks[0])
