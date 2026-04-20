"""
app.py — RAIN Agency Chatbot
Run with:  streamlit run app.py
Set key:   export ANTHROPIC_API_KEY=sk-ant-your-key-here
"""

import os
import streamlit as st
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=sk-ant-your-key-here")
    st.stop()

Settings.llm = Anthropic(
    model="claude-sonnet-4-5",
    api_key=api_key,
    max_tokens=1024,
    system_prompt=(
        "You are a helpful assistant for RAIN, a digital marketing agency "
        "specializing in campaigns for banks and credit unions. "
        "Answer questions about RAIN's services, clients, case studies, "
        "approach, and expertise using only the information provided to you. "
        "Be friendly, clear, and concise. "
        "If something is not covered in the provided information, say so honestly. "
        "Always end every response with this exact line on a new line: "
        "'For more information, visit [rainlocal.com](https://www.rainlocal.com) "
        "or email support@rainlocal.com'"
    ),
)

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


@st.cache_resource
def load_index():
    if not os.path.exists("storage/"):
        return None
    storage_context = StorageContext.from_defaults(persist_dir="storage/")
    return load_index_from_storage(storage_context)

index = load_index()

if index is None:
    st.error("No index found. Please run `python ingest.py` first.")
    st.stop()


@st.cache_resource
def get_query_engine(_index):
    return _index.as_query_engine(similarity_top_k=3, response_mode="compact")

query_engine = get_query_engine(index)


st.set_page_config(
    page_title="RAIN — Smart Marketing Assistant",
    page_icon="🌧",
    layout="centered",
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #07101f 0%, #0b1a35 50%, #0d1428 100%);
    min-height: 100vh;
}

[data-testid="stMainBlockContainer"] {
    max-width: 780px;
    padding: 2.5rem 1.5rem 0;
}

/* ── Card header ── */
.chat-header {
    background: linear-gradient(135deg, #1a3680 0%, #1565c0 100%);
    padding: 20px 28px 18px;
    border-radius: 18px 18px 0 0;
    border: 1px solid #1e3f7a;
    border-bottom: none;
    display: flex;
    align-items: center;
    gap: 14px;
}
.chat-avatar {
    width: 44px; height: 44px;
    background: rgba(255,255,255,0.15);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.chat-header h2 { margin: 0; color: #fff; font-size: 1.1rem; font-weight: 700; }
.chat-header p  { margin: 3px 0 0; color: rgba(255,255,255,0.6); font-size: 0.76rem; }
.dot { display:inline-block; width:7px; height:7px; background:#4caf50;
       border-radius:50%; margin-right:5px; vertical-align:middle; }

/* ── Messages scroll area ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #1e3f7a !important;
    border-top: none !important;
    border-bottom: none !important;
    border-radius: 0 !important;
    background: #080f1e !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stVerticalBlockBorderWrapper"] > div > div {
    background: #080f1e !important;
}

/* ── Chat bubbles ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 16px !important;
}

/* user — right, blue */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
  [data-testid="stMarkdownContainer"] p {
    background: #1a3a8f !important;
    color: #fff !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 10px 15px !important;
    display: inline-block;
    max-width: 75%;
    float: right;
    clear: both;
    line-height: 1.5;
    margin: 0;
}

/* assistant — left, dark */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
  [data-testid="stMarkdownContainer"] p {
    background: #0e1c3a !important;
    color: #dde3f0 !important;
    border-radius: 16px 16px 16px 4px !important;
    padding: 10px 15px !important;
    display: inline-block;
    max-width: 75%;
    line-height: 1.5;
    margin: 0;
}

[data-testid="stChatMessageContent"] { max-width: 88% !important; }

/* ── Input bar — visually part of the card ── */
[data-testid="stBottom"] {
    background: #080f1e !important;
    border-left: 1px solid #1e3f7a !important;
    border-right: 1px solid #1e3f7a !important;
    border-bottom: 1px solid #1e3f7a !important;
    border-top: 1px solid #1a3568 !important;
    border-radius: 0 0 18px 18px !important;
    padding: 14px 20px 18px !important;
    box-shadow: 0 12px 40px rgba(0,10,40,0.6) !important;
}

[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stChatInput"] textarea {
    background: #0c1528 !important;
    color: #cdd8f0 !important;
    border: 1.5px solid #1e3f7a !important;
    border-radius: 14px !important;
    font-size: 0.94rem !important;
    padding: 14px 18px !important;
    line-height: 1.5 !important;
    min-height: 52px !important;
    resize: none !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #2060c0 !important;
    box-shadow: 0 0 0 3px rgba(30,80,180,0.2) !important;
    outline: none !important;
}

[data-testid="stChatInput"] textarea::placeholder { color: #3a506a !important; }

[data-testid="stChatInputSubmitButton"] button {
    background: #1a55b0 !important;
    border-radius: 10px !important;
    border: none !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    background: #2060c8 !important;
}

/* ── Kill Streamlit loading dim/overlay ── */
[data-testid="stApp"] { opacity: 1 !important; }
[data-testid="stApp"] > * { opacity: 1 !important; }
[data-stale] { opacity: 1 !important; }
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Typing indicator dots ── */
.typing-bubble {
    background: #1e2336;
    border-radius: 16px 16px 16px 4px;
    padding: 12px 18px;
    display: inline-flex;
    gap: 5px;
    align-items: center;
}
.typing-bubble span {
    width: 7px; height: 7px;
    background: #556090;
    border-radius: 50%;
    display: inline-block;
    animation: blink 1.2s infinite;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.2s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.85); }
    40%           { opacity: 1;   transform: scale(1); }
}

/* ── Clear button ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #1e3fa0 !important;
    color: #556080 !important;
    border-radius: 8px !important;
    font-size: 0.76rem !important;
    padding: 3px 12px !important;
    margin-top: 6px;
}
.stButton > button:hover {
    border-color: #4060b0 !important;
    color: #8899cc !important;
}
</style>
""", unsafe_allow_html=True)


# ── Header ──
st.markdown("""
<div class="chat-header">
  <div class="chat-avatar">🌧</div>
  <div>
    <h2>RAIN Assistant</h2>
    <p>World-Class Digital Marketing Agency</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# capture input first (renders sticky at bottom regardless of position)
prompt = st.chat_input("Ask anything about RAIN...")

# ── Bordered chat box ──
with st.container(height=480, border=True):

    # Welcome message on first load
    if not st.session_state.messages and not prompt:
        with st.chat_message("assistant"):
            st.markdown("Hi! I'm the RAIN assistant. Ask me anything about RAIN's services, campaigns, clients, or results.")

    # Render existing history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # New exchange — user bubble appears immediately, typing dots, then answer
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            typing = st.empty()
            typing.markdown(
                '<div class="typing-bubble"><span></span><span></span><span></span></div>',
                unsafe_allow_html=True,
            )

            response = query_engine.query(prompt)
            answer = str(response)

            if response.source_nodes:
                sources = list({
                    node.metadata.get("file_name", "").replace(".txt", "").replace("_", " ")
                    for node in response.source_nodes
                    if node.metadata.get("file_name")
                })
                if sources:
                    answer += f"\n\n*Source: {' · '.join(sources)}*"

            typing.empty()
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


# ── Clear button ──
if st.session_state.messages:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col3:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()
