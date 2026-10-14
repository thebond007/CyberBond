from dotenv import load_dotenv
load_dotenv()

from models import get_model
from rag.chain import rag_stream

llm = get_model()
stream, sources = rag_stream(llm, "What is SQL injection?")

for token in stream:
    print(token, end="", flush=True)

print("\n\nSources:")
for s in sources:
    print(" -", s)