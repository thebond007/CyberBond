"""CSS theme for CyberBond — charcoal & gold, minimal blue."""

THEME_CSS = """
<style>
:root {
    --bg-dark: #121212;
    --bg-panel: #1c1c1c;
    --gold: #c9a227;
    --gold-soft: #e0bf5a;
    --text-muted: #a8a8a8;
}

.stApp {
    background: linear-gradient(180deg, #0e0e0e 0%, #161616 100%);
}

section[data-testid="stSidebar"] {
    background-color: #0f0f0f;
    border-right: 1px solid rgba(201, 162, 39, 0.25);
}

section[data-testid="stSidebar"] * {
    color: #e6e6e6 !important;
}

.cb-title {
    font-size: 2rem;
    font-weight: 800;
    color: var(--gold-soft);
    letter-spacing: 1px;
    margin-bottom: 0;
}

.cb-subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0;
    margin-bottom: 1.2rem;
}

div[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 0.4rem 0.2rem;
    margin-bottom: 0.4rem;
}

.stChatMessage {
    background-color: var(--bg-panel);
}

div[data-testid="stChatInput"] textarea {
    background-color: var(--bg-panel) !important;
    color: white !important;
    border: 1px solid rgba(201, 162, 39, 0.4) !important;
    border-radius: 12px !important;
}

button[kind="primary"], .stButton > button {
    background-color: var(--gold) !important;
    color: #121212 !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}

.stButton > button:hover {
    background-color: var(--gold-soft) !important;
}

hr {
    border-color: rgba(201, 162, 39, 0.25) !important;
}

div[data-testid="stAlert"] {
    background-color: #1c1c1c !important;
    border: 1px solid rgba(201, 162, 39, 0.35) !important;
}

div[data-testid="stAlert"] * {
    color: #e6e6e6 !important;
}

div[data-testid="stAlert"] em {
    color: var(--gold-soft) !important;
}
</style>
"""