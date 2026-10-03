import os

os.environ["PINECONE_API_KEY"] = "pcsk_37GL85_9XcD2V9jcXRZh8yX4CqcpahVC2pGpCqng6Ra6MdxJ4mbUroKJ5e7U3uBG2hUJE3"
os.environ["GROQ_API_KEY"] = "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"
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
INDEX_NAME = "medical-chatbot"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    embeddings = get_embeddings()
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})
    
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain