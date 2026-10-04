import os
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="MediAI",
    page_icon="⚕️",
    layout="wide"
)

# =====================================================
# API KEYS
# =====================================================

if "PINECONE_API_KEY" in st.secrets:
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from bot import get_rag_chain


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

/* Hide Streamlit Stuff */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* App */
.stApp{
    background:#0b1220;
    color:white;
}

/* Width */
.block-container{
    max-width:1100px;
    padding-top:2rem;
    padding-bottom:8rem;
}

/* Fonts */
html, body, [class*="css"]{
    font-family: Inter, sans-serif;
}

/* Hero */
.hero{
    text-align:center;
    padding:40px 20px 20px 20px;
}

.hero-title{
    font-size:4rem;
    font-weight:800;
    color:white;
    margin-bottom:8px;
}

.hero-subtitle{
    font-size:1.2rem;
    color:#94a3b8;
    max-width:700px;
    margin:auto;
    line-height:1.7;
}

/* Metrics */
.metric-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px;
    padding:20px;
    text-align:center;
    backdrop-filter:blur(15px);
}

.metric-title{
    color:#94a3b8;
    font-size:0.9rem;
}

.metric-value{
    color:white;
    font-size:1.5rem;
    font-weight:700;
}

/* Welcome */
.welcome{
    margin-top:25px;
    padding:35px;
    text-align:center;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    backdrop-filter:blur(15px);
}

.welcome h2{
    color:white;
}

.welcome p{
    color:#94a3b8;
}

/* Chat Messages */
[data-testid="stChatMessage"]{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px;
    padding:12px;
    margin-bottom:14px;
}

/* Buttons */
.stButton button{
    width:100%;
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.1);
    background:#111827;
    color:white;
    min-height:55px;
    transition:0.2s;
}

.stButton button:hover{
    border-color:#14b8a6;
    color:#14b8a6;
}

/* Chat Input */
[data-testid="stChatInput"]{
    background:#111827;
    border-radius:18px;
}

/* Disclaimer */
.disclaimer{
    margin-top:40px;
    color:#64748b;
    text-align:center;
    font-size:0.85rem;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_chain():
    return get_rag_chain()

chain = load_chain()

# =====================================================
# STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "example_prompt" not in st.session_state:
    st.session_state.example_prompt = None


# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        ⚕️ MediAI
    </div>

    <div class="hero-subtitle">
        AI-powered medical knowledge assistant.
        Search symptoms, diseases, medications,
        treatments and evidence-based medical information.
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# METRICS
# =====================================================

m1,m2,m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Knowledge Base</div>
        <div class="metric-value">Medical RAG</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Search</div>
        <div class="metric-value">Pinecone</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Model</div>
        <div class="metric-value">Groq LLM</div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# EMPTY SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">
        <h2>What would you like to know?</h2>
        <p>
        Ask a medical question or choose one of the examples below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Suggested Questions")

    c1,c2 = st.columns(2)

    with c1:

        if st.button("🫀 Common symptoms of hypertension"):
            st.session_state.example_prompt = (
                "What are the common symptoms of hypertension?"
            )

        if st.button("💊 How do antibiotics work?"):
            st.session_state.example_prompt = (
                "How do antibiotics work?"
            )

    with c2:

        if st.button("🩸 Causes of iron deficiency anemia"):
            st.session_state.example_prompt = (
                "What causes iron deficiency anemia?"
            )

        if st.button("🧠 Migraine vs headache"):
            st.session_state.example_prompt = (
                "Explain the difference between migraine and headache."
            )


# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    avatar = "🧑" if message["role"] == "user" else "⚕️"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# =====================================================
# INPUT
# =====================================================

typed_prompt = st.chat_input(
    "Ask a medical question..."
)

prompt = typed_prompt or st.session_state.example_prompt

# =====================================================
# RESPONSE
# =====================================================

if prompt:

    st.session_state.example_prompt = None

    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message(
        "assistant",
        avatar="⚕️"
    ):

        with st.spinner(
            "Searching medical knowledge..."
        ):

            try:

                result = chain.invoke(prompt)

                if isinstance(result, dict):

                    response = (
                        result.get("answer")
                        or result.get("result")
                        or str(result)
                    )

                else:
                    response = str(result)

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":response
                    }
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="disclaimer">
Medical information provided by AI is for educational purposes only and
should not replace professional medical advice, diagnosis or treatment.
</div>
""", unsafe_allow_html=True)
