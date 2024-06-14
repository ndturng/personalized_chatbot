from data.pdf_process import load_pdf_from_path
from langchain_core.documents.base import Document


def test_load_pdf_from_path():
    path = "data/storage"
    docs = load_pdf_from_path(path)
    assert len(docs) == 160
    assert isinstance(docs[0], Document)
    assert isinstance(docs[0].page_content, str)
    assert isinstance(docs[0].metadata, dict)