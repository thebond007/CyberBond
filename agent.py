"""Tool-calling agent loop for CyberBond (streams tokens, runs tools)."""
import re

from langchain_core.messages import SystemMessage, ToolMessage

from tools import ALL_TOOLS

TOOLS_BY_NAME = {t.name: t for t in ALL_TOOLS}
MAX_STEPS = 5
HISTORY_LIMIT = 10

AGENT_PROMPT = """You are CyberBond, a digital forensics and cybersecurity assistant for a cyber security faculty member and students.

Rules:
- For any digital forensics concept or theory question (chain of custody, file systems, investigation process, digital evidence), call search_notes first and answer ONLY from what it returns. If the notes don't cover it, say: "I don't have that in the knowledge base."
- If the user pastes text to hash, a timestamp to convert, logs to scan for IOCs, or file header bytes, use the matching tool and explain the result briefly.
- For greetings, thanks, or follow-ups about the conversation itself, reply normally without tools.
- Be clear and structured. Never invent facts about the user's notes.
- When explaining hashes, note that MD5 and SHA-1 are collision-broken: fine for quick integrity checks, but SHA-256 is preferred for evidence, and none of these plain hashes are suitable for password storage."""


def run_agent(llm, history):
    """Generator yielding dict events:
    {"type": "token", "text": str}
    {"type": "tool", "name": str, "args": dict}
    {"type": "sources", "sources": list[str]}
    """
    llm_tools = llm.bind_tools(ALL_TOOLS)
    convo = [m for m in history if not isinstance(m, SystemMessage)][-HISTORY_LIMIT:]
    messages = [SystemMessage(content=AGENT_PROMPT)] + convo
    sources = []

    for _ in range(MAX_STEPS):
        full = None
        for chunk in llm_tools.stream(messages):
            full = chunk if full is None else full + chunk
            if isinstance(chunk.content, str) and chunk.content:
                yield {"type": "token", "text": chunk.content}

        if full is None or not full.tool_calls:
            break

        messages.append(full)
        for call in full.tool_calls:
            yield {"type": "tool", "name": call["name"], "args": call["args"]}
            tool = TOOLS_BY_NAME.get(call["name"])
            try:
                result = tool.invoke(call["args"]) if tool else "Unknown tool."
            except Exception as e:
                result = f"Tool error: {e}"
            if call["name"] == "search_notes":
                for label in re.findall(r"^\[(.+?)\]$", str(result), flags=re.M):
                    if label not in sources:
                        sources.append(label)
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    yield {"type": "sources", "sources": sources}