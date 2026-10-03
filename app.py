import streamlit as st
from bot import rag_chain

st.set_page_config(page_title="Medical AI Assistant", page_icon="⚕️")
st.title("⚕️ Medical Knowledge Assistant")

# Cache the loaded RAG chain using st.cache_resource
@st.cache_resource
def load_chain():
    return rag_chain

chain = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a medical question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Searching medical records..."):
            try:
                response = chain.invoke(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")