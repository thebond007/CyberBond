"""Retrieval -> prompt -> LLM. Returns a streaming answer plus sources."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.retriever import retrieve

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are CyberBond, a cybersecurity and digital forensics assistant. "
     "Answer using ONLY the context below. If the context does not contain "
     "the answer, say you don't have that in the knowledge base. "
     "Be clear and structured.\n\nContext:\n{context}"),
    ("human", "{question}"),
])


def format_context(docs):
    return "\n\n".join(d.page_content for d in docs)


def format_sources(docs):
    seen = []
    for d in docs:
        name = d.metadata.get("source", "unknown").split("\\")[-1]
        page = d.metadata.get("page")
        label = f"{name} (p.{page + 1})" if isinstance(page, int) else name
        if label not in seen:
            seen.append(label)
    return seen


def rag_stream(llm, question: str):
    """Returns (token_stream, sources)."""
    docs = retrieve(question)
    chain = PROMPT | llm | StrOutputParser()
    stream = chain.stream({"context": format_context(docs), "question": question})
    return stream, format_sources(docs)