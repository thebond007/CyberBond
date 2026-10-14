"""Main chat area UI for CyberBond."""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import config
import session as session_mgr
from models import get_model
from agent import run_agent

NO_ANSWER_MARKER = "knowledge base"
TOOL_LABELS = {
    "search_notes": "Searched your notes",
    "calculate_hashes": "Calculated hashes",
    "convert_timestamp": "Converted timestamp",
    "extract_iocs": "Extracted IOCs",
    "check_file_signature": "Checked file signature",
}


def _show_extras(tools, sources):
    if tools:
        st.caption("🔧 " + " · ".join(TOOL_LABELS.get(t, t) for t in tools))
    if sources:
        with st.expander("📚 Sources"):
            for s in sources:
                st.markdown(f"- {s}")


def render_chat():
    st.markdown(f'<p class="cb-title">{config.APP_ICON} {config.APP_TITLE}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="cb-subtitle">{config.APP_SUBTITLE}</p>', unsafe_allow_html=True)

    active = session_mgr.get_active_session()
    display_messages = [m for m in active["messages"] if not isinstance(m, SystemMessage)]

    if not display_messages:
        st.info(
            "Ask about digital forensics from your course notes, or paste text to "
            "hash, a timestamp to convert, logs to scan for IOCs, or file header "
            "bytes to identify. Try: *\"What is chain of custody?\"*"
        )

    for msg in display_messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        avatar = "🧑‍💻" if role == "user" else "🛡️"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg.content)
            if role == "assistant":
                _show_extras(
                    msg.additional_kwargs.get("tools"),
                    msg.additional_kwargs.get("sources"),
                )

    prompt = st.chat_input("Ask CyberBond about security, forensics, or hardening...")

    if prompt:
        active["messages"].append(HumanMessage(content=prompt))

        if active["title"] == "New chat":
            active["title"] = (prompt[:32] + "…") if len(prompt) > 32 else prompt

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        tools_used, sources = [], []
        with st.chat_message("assistant", avatar="🛡️"):
            placeholder = st.empty()
            full_response = ""
            try:
                model = get_model()
                for event in run_agent(model, active["messages"]):
                    if event["type"] == "token":
                        full_response += event["text"]
                        placeholder.markdown(full_response + "▌")
                    elif event["type"] == "tool":
                        if event["name"] not in tools_used:
                            tools_used.append(event["name"])
                    elif event["type"] == "sources":
                        sources = event["sources"]
                placeholder.markdown(full_response)

                if NO_ANSWER_MARKER in full_response.lower():
                    sources = []
                _show_extras(tools_used, sources)
            except Exception as e:
                full_response = f"⚠️ Error talking to the model: `{e}`"
                placeholder.markdown(full_response)
                tools_used, sources = [], []

        active["messages"].append(
            AIMessage(
                content=full_response,
                additional_kwargs={"tools": tools_used, "sources": sources},
            )
        )
        st.rerun()