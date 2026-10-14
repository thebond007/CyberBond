"""Model loading logic for CyberBond."""

import streamlit as st
from langchain_groq import ChatGroq
import config


@st.cache_resource(show_spinner=False)
def get_model():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_NEW_TOKENS,
    )