import os
import streamlit as st
from bot import get_rag_chain

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="MediAI",
    page_icon="⚕️",
    layout="wide"
)

# ======================================================
# ENV VARIABLES
# ======================================================

if "PINECONE_API_KEY" in st.secrets:
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

/* Hide Streamlit branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Page */
.stApp {
    background: #0B1220;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.hero p {
    color: #94A3B8;
    font-size: 1.15rem;
    max-width: 700px;
    margin: auto;
    line-height: 1.7;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.25rem;
    text-align: center;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 12px;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 14px;
    min-height: 55px;
    background: #111827;
    color: white;
    border: 1px solid #1F2937;
}

.stButton button:hover {
    border-color: #14B8A6;
    color: #14B8A6;
}

/* Section Title */
.section-title {
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

/* Footer */
.footer {
    text-align:center;
    color:#64748B;
    margin-top:40px;
    font-size:0.9rem;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD CHAIN
# ======================================================

@st.cache_resource
def load_chain():
    return get_rag_chain()

chain = load_chain()

# ======================================================
# SESSION STATE
# ======================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sample_prompt" not in st.session_state:
    st.session_state.sample_prompt = None

# ======================================================
# HERO
# ======================================================

st.markdown("""
<div class="hero">
    <h1>⚕️ MediAI</h1>
    <p>
        AI-powered medical knowledge assistant for symptoms,
        diseases, medications, treatments and evidence-based
        healthcare information.
    </p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# TOP INFO CARDS
# ======================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card">
        <h3>📚 Knowledge Base</h3>
        <p>Medical Documents</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card">
        <h3>🔍 Retrieval</h3>
        <p>Pinecone Vector Search</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card">
        <h3>🤖 AI Model</h3>
        <p>Groq Powered</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CLEAR CHAT
# ======================================================

col1, col2 = st.columns([8,1])

with col2:
    if st.button("🗑 Clear"):
        st.session_state.messages = []
        st.rerun()

# ======================================================
# EMPTY STATE
# ======================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="section-title">Suggested Questions</div>',
        unsafe_allow_html=True
    )

    a, b = st.columns(2)

    with a:
        if st.button("🫀 Symptoms of Hypertension"):
            st.session_state.sample_prompt = (
                "What are the common symptoms of hypertension?"
            )

        if st.button("💊 How do antibiotics work?"):
            st.session_state.sample_prompt = (
                "How do antibiotics work?"
            )

    with b:
        if st.button("🩸 Iron Deficiency Anemia"):
            st.session_state.sample_prompt = (
                "What causes iron deficiency anemia?"
            )

        if st.button("🧠 Migraine vs Headache"):
            st.session_state.sample_prompt = (
                "Explain the difference between migraine and headache."
            )

# ======================================================
# CHAT HISTORY
# ======================================================

for msg in st.session_state.messages:

    avatar = "🧑" if msg["role"] == "user" else "⚕️"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ======================================================
# INPUT
# ======================================================

typed_prompt = st.chat_input(
    "Ask a medical question..."
)

prompt = typed_prompt or st.session_state.sample_prompt

# ======================================================
# GENERATE RESPONSE
# ======================================================

if prompt:

    st.session_state.sample_prompt = None

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("assistant", avatar="⚕️"):

        with st.spinner("Searching medical knowledge..."):

            try:

                result = chain.invoke(prompt)

                if isinstance(result, dict):
                    answer = (
                        result.get("answer")
                        or result.get("result")
                        or result.get("output")
                        or str(result)
                    )
                else:
                    answer = str(result)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Error: {e}")

# ======================================================
# FOOTER
# ======================================================

st.markdown("""
<div class="footer">
⚠️ This assistant provides educational medical information and should not replace professional medical advice.
</div>
""", unsafe_allow_html=True)
