"""CyberBond — entry point."""

import streamlit as st
from dotenv import load_dotenv

import config
from theme import THEME_CSS
import session as session_mgr
from ui.sidebar import render_sidebar
from ui.chat import render_chat

load_dotenv()

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(THEME_CSS, unsafe_allow_html=True)

session_mgr.init_sessions()
session_mgr.ensure_active_session()

render_sidebar()
render_chat()