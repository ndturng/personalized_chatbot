import random
from data.pdf_process import load_pdf_from_path, slpit_text
from langchain_core.documents.base import Document


def test_load_pdf_from_path():
    data_path = "data/storage"
    docs = load_pdf_from_path(data_path)
    assert len(docs) == 160
    assert isinstance(docs[0], Document)
    assert isinstance(docs[0].page_content, str)
    assert isinstance(docs[0].metadata, dict)


def test_slpit_text():
    data_path = "data/storage"
    docs = load_pdf_from_path(data_path)
    text_chunks = slpit_text(docs)
    assert len(text_chunks) != len(docs)
    # get random text chunk
    num = random.randint(0, len(text_chunks) - 1)
    assert len(text_chunks[num].page_content) <= 1000  # the chunk size is 1000