"""Load the Chroma store and return the top-k relevant chunks."""
import sys
from functools import lru_cache
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from rag.ingest import DB_DIR, EMBED_MODEL


@lru_cache(maxsize=1)
def get_db():
    """Load embeddings + Chroma once, reuse for every query."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)


def get_retriever(k: int = 4):
    return get_db().as_retriever(search_kwargs={"k": k})


def retrieve(query: str, k: int = 4):
    """Top-k chunks with exact-duplicate text removed."""
    retriever = get_retriever(k=k * 2)  # fetch extra, then dedupe
    seen, unique = set(), []
    for doc in retriever.invoke(query):
        key = doc.page_content.strip()
        if key not in seen:
            seen.add(key)
            unique.append(doc)
    return unique[:k]


if __name__ == "__main__":
    query = input("Ask something from your DF notes: ")
    for i, doc in enumerate(retrieve(query), start=1):
        src = doc.metadata.get("source", "unknown").split("\\")[-1]
        page = doc.metadata.get("page", "-")
        print(f"\n--- Result {i} | {src} | page {page} ---")
        print(doc.page_content[:400])
