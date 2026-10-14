"""Ingest documents: load -> chunk -> embed -> store in Chroma."""
import shutil
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "data" / "docs"
DB_DIR = ROOT / "data" / "vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    docs = []
    for path in DOCS_DIR.rglob("*"):
        suffix = path.suffix.lower()
        try:
            if suffix == ".pdf":
                docs.extend(PyPDFLoader(str(path)).load())
            elif suffix == ".docx":
                docs.extend(Docx2txtLoader(str(path)).load())
            elif suffix in {".txt", ".md"}:
                docs.extend(TextLoader(str(path), encoding="utf-8").load())
            else:
                continue
            print(f"Loaded: {path.name}")
        except Exception as e:
            print(f"Skipped {path.name}: {e}")
    return docs


def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return splitter.split_documents(docs)


def build_vectorstore(chunks):
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)  # rebuild clean so you never get duplicates
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma.from_documents(
        chunks, embeddings, persist_directory=str(DB_DIR)
    )


def main():
    docs = load_documents()
    if not docs:
        print(f"No documents found in {DOCS_DIR}. Add PDF/DOCX/TXT/MD files first.")
        return
    chunks = chunk_documents(docs)
    build_vectorstore(chunks)
    print(f"\nIngested {len(docs)} pages/docs -> {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
    