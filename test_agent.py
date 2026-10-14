from dotenv import load_dotenv
load_dotenv()

from models import get_model
from agent import run_agent
from langchain_core.messages import HumanMessage

llm = get_model()

questions = [
    "hi",
    "What is chain of custody?",
    "Give me the SHA-256 of the text: evidence01",
    "Convert timestamp 133000000000000000",
    "What is SQL injection?",
]

for q in questions:
    print(f"\n=== {q} ===")
    for ev in run_agent(llm, [HumanMessage(content=q)]):
        if ev["type"] == "token":
            print(ev["text"], end="", flush=True)
        elif ev["type"] == "tool":
            print(f"\n[tool: {ev['name']} {ev['args']}]")
        elif ev["type"] == "sources":
            print(f"\n[sources: {ev['sources']}]")