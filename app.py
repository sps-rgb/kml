```python
import os
import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD SECRETS
# ---------------------------------------------------
if "PINECONE_API_KEY" in st.secrets:
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


from bot import get_rag_chain


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown(
    """
    <style>

    /* Global */
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(20, 184, 166, 0.08), transparent 25%),
            radial-gradient(circle at bottom left, rgba(59, 130, 246, 0.08), transparent 25%),
            #f7fafc;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* Hide default Streamlit footer/menu */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Header area */
    .medical-header {
        padding: 22px 26px;
        border-radius: 20px;
        margin-bottom: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(13, 148, 136, 0.95),
                rgba(37, 99, 235, 0.90)
            );

        box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.08);
    }

    .medical-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }

    .medical-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 1rem;
    }

    /* Welcome card */
    .welcome-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15, 118, 110, 0.12);
        border-radius: 22px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 8px 28px rgba(15, 23, 42, 0.06);
        margin-top: 20px;
        margin-bottom: 25px;
    }

    .welcome-icon {
        font-size: 3rem;
    }

    .welcome-card h2 {
        color: #0f172a;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .welcome-card p {
        color: #64748b;
        max-width: 650px;
        margin: auto;
        line-height: 1.6;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 18px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0px 4px 14px rgba(15,23,42,0.04);
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.95);
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 44px;
        font-weight: 600;

        border: 1px solid rgba(13, 148, 136, 0.22);
        background: white;

        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #0d9488;
        color: #0d9488;
        transform: translateY(-1px);
        box-shadow: 0px 5px 15px rgba(13,148,136,0.10);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #f0fdfa 0%,
                #eff6ff 100%
            );
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Small status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        padding: 6px 12px;
        border-radius: 999px;

        background: #dcfce7;
        color: #166534;

        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 10px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
    }

    /* Disclaimer */
    .disclaimer {
        margin-top: 25px;
        padding: 13px 16px;

        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 12px;

        color: #9a3412;
        font-size: 0.84rem;
        line-height: 1.45;
    }

    /* Section labels */
    .section-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# RAG CHAIN
# ---------------------------------------------------
@st.cache_resource
def load_chain():
    return get_rag_chain()


chain = load_chain()


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.markdown("## ⚕️ MediAssist AI")

    st.caption(
        "AI-powered medical knowledge assistant using retrieval-augmented generation."
    )

    st.markdown(
        """
        <div class="status-badge">
            <span class="status-dot"></span>
            AI System Online
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 💡 What you can ask")

    st.markdown(
        """
        - Symptoms and medical conditions
        - Medication information
        - Disease explanations
        - Medical terminology
        - General health knowledge
        """
    )

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.selected_prompt = None
        st.rerun()

    st.markdown(
        """
        <div class="disclaimer">
            <b>⚠️ Medical Disclaimer</b><br><br>
            This AI assistant provides general medical information and is
            not a substitute for professional medical advice, diagnosis,
            or treatment.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------
st.markdown(
    """
    <div class="medical-header">
        <h1>⚕️ Medical Knowledge Assistant</h1>

        <p>
            Ask medical questions and get contextual answers powered by
            AI and retrieved medical knowledge.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# EMPTY STATE / QUICK QUESTIONS
# ---------------------------------------------------
if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-icon">🩺</div>

            <h2>How can I help you today?</h2>

            <p>
                Ask a medical question below or choose one of the example
                questions to get started.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">Suggested questions</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🫀 What are the common symptoms of hypertension?"
        ):
            st.session_state.selected_prompt = (
                "What are the common symptoms of hypertension?"
            )

        if st.button(
            "💊 How do antibiotics work?"
        ):
            st.session_state.selected_prompt = (
                "How do antibiotics work?"
            )

    with col2:

        if st.button(
            "🩸 What causes iron deficiency anemia?"
        ):
            st.session_state.selected_prompt = (
                "What causes iron deficiency anemia?"
            )

        if st.button(
            "🧠 Explain the difference between migraine and headache"
        ):
            st.session_state.selected_prompt = (
                "Explain the difference between migraine and headache."
            )


# ---------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------
for message in st.session_state.messages:

    avatar = "🧑" if message["role"] == "user" else "⚕️"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# ---------------------------------------------------
# INPUT
# ---------------------------------------------------
typed_prompt = st.chat_input(
    "Ask a medical question..."
)

prompt = typed_prompt or st.session_state.selected_prompt


# ---------------------------------------------------
# PROCESS QUESTION
# ---------------------------------------------------
if prompt:

    # Reset preset question
    st.session_state.selected_prompt = None

    # Display user question
    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # AI response
    with st.chat_message(
        "assistant",
        avatar="⚕️"
    ):

        with st.spinner(
            "🔎 Searching medical knowledge..."
        ):

            try:

                response = chain.invoke(prompt)

                # Handle different possible chain output formats
                if isinstance(response, dict):

                    response_text = (
                        response.get("answer")
                        or response.get("result")
                        or response.get("output")
                        or str(response)
                    )

                else:
                    response_text = str(response)

                st.markdown(response_text)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response_text
                    }
                )

            except Exception as e:

                st.error(
                    "⚠️ I couldn't generate a response."
                )

                with st.expander(
                    "Technical details"
                ):
                    st.code(str(e))


    # Forces page to redraw cleanly after preset button interaction
    if typed_prompt is None:
        st.rerun()
```
