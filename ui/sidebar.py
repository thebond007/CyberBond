"""Sidebar UI for CyberBond."""

import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
import session as session_mgr


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛡️ CyberBond")
        st.caption("Cybersecurity chat assistant")

        if st.button("➕ New chat", use_container_width=True):
            session_mgr.new_session()
            st.rerun()

        st.markdown("---")
        st.markdown("**Chats**")

        session_ids = list(st.session_state.sessions.keys())[::-1]
        for sid in session_ids:
            sess = st.session_state.sessions[sid]
            label = sess["title"]
            is_active = sid == st.session_state.active_session
            prefix = "🟡 " if is_active else "⚪ "
            if st.button(prefix + label, key=f"sess_{sid}", use_container_width=True):
                st.session_state.active_session = sid
                st.rerun()

        st.markdown("---")

        active = session_mgr.get_active_session()
        chat_msgs = [m for m in active["messages"] if not isinstance(m, SystemMessage)]

        if chat_msgs:
            export_lines = []
            for m in chat_msgs:
                who = "You" if isinstance(m, HumanMessage) else "CyberBond"
                export_lines.append(f"**{who}:** {m.content}\n")
            export_text = "\n".join(export_lines)
            st.download_button(
                "⬇️ Export chat (.md)",
                data=export_text,
                file_name=f"cyberbond_chat_{active['created'].replace(' ', '_').replace(':', '')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        if st.button("🗑️ Delete this chat", use_container_width=True):
            del st.session_state.sessions[st.session_state.active_session]
            st.session_state.active_session = None
            session_mgr.ensure_active_session()
            st.rerun()