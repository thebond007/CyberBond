"""Model loading logic for CyberBond."""

import os
import streamlit as st
from langchain_groq import ChatGroq
import config


def _load_api_key():
    if os.environ.get("GROQ_API_KEY"):
        return
    try:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass  # no secrets file locally; .env handles it


@st.cache_resource(show_spinner=False)
def get_model():
    _load_api_key()
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_NEW_TOKENS,
    )