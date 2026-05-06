import os
import streamlit as st

# Configuration Constants
INDEX_DIR = "faiss_index_storage"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 10

GROQ_MODELS = [
    "llama-3.3-70b-versatile",     
    "llama-3.1-70b-versatile",     
    "llama-3.1-8b-instant",        
    "mixtral-8x7b-32768",          
    "gemma2-9b-it",                
    "llama3-70b-8192",             
    "llama3-8b-8192",              
]

# Dependency Checks
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from langchain_community.llms import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def _normalize_api_key(value):
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None

def get_api_keys():
    """Retrieve API keys securely"""
    groq_key = _normalize_api_key(os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None))
    openai_key = _normalize_api_key(os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None))
    gemini_key = _normalize_api_key(os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None))
    return bool(groq_key), bool(openai_key), bool(gemini_key), groq_key, openai_key, gemini_key