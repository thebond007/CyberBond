"""Session state management for CyberBond's multi-chat sidebar."""

import uuid
from datetime import datetime
import streamlit as st
from langchain_core.messages import SystemMessage
import config


def init_sessions():
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    if "active_session" not in st.session_state:
        st.session_state.active_session = None


def new_session():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {
        "title": "New chat",
        "messages": [SystemMessage(content=config.SYSTEM_PROMPT)],
        "created": datetime.now().strftime("%d %b, %H:%M"),
    }
    st.session_state.active_session = sid


def ensure_active_session():
    if (
        st.session_state.active_session is None
        or st.session_state.active_session not in st.session_state.sessions
    ):
        if st.session_state.sessions:
            st.session_state.active_session = list(st.session_state.sessions.keys())[-1]
        else:
            new_session()


def get_active_session():
    return st.session_state.sessions[st.session_state.active_session]