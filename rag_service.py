import os
import shutil
import streamlit as st
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from config import EMBEDDING_MODEL_NAME
from logger import log_event

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def build_or_load_faiss(docs: List[Document], index_dir: str, force_rebuild: bool = False):
    embeddings = get_embeddings()
    if os.path.exists(index_dir) and not force_rebuild:
        try:
            db = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
            log_event("Loaded existing FAISS index")
            return db
        except Exception as e:
            log_event(f"Failed to load index: {e}", "WARNING")
            shutil.rmtree(index_dir, ignore_errors=True)
            
    log_event(f"Building FAISS index from {len(docs)} documents")
    db = FAISS.from_documents(docs, embeddings)
    os.makedirs(index_dir, exist_ok=True)
    db.save_local(index_dir)
    return db

def get_llm_instance(api_key, model_name, provider="groq"):
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.0)
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.0, max_tokens=4096)
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(api_key=api_key, model=model_name, temperature=0.0, max_tokens=4096)


def is_auth_error(error: Exception) -> bool:
    message = str(error).lower()
    return "invalid_api_key" in message or "invalid api key" in message or "401" in message


def is_quota_error(error: Exception) -> bool:
    message = str(error).lower()
    return "insufficient_quota" in message or "exceeded your current quota" in message or "429" in message

def process_query(latest_query, retriever, llm_instance):
    prompt = ChatPromptTemplate.from_template("""
    You are an expert AI assistant helping users understand their documents.
    Context from the uploaded documents:
    {context}
    Question: {input}
    Instructions:
    - First, carefully review the Context above for relevant information
    - Answer based ONLY on the context provided.
    Answer:
    """)
    document_chain = create_stuff_documents_chain(llm_instance, prompt)
    qa_chain = create_retrieval_chain(retriever, document_chain)
    return qa_chain.invoke({"input": latest_query})