from pathlib import Path
from setuptools import setup

BASE_DIR = Path(__file__).parent

requirements = [
    line.strip()
    for line in (BASE_DIR / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]

setup(
    name="universal-rag-chatbot",
    version="0.1.0",
    description="Streamlit-based RAG chatbot with LangChain and FAISS",
    py_modules=["app", "config", "document_service", "logger", "rag_service", "ui_components"],
    install_requires=requirements,
    python_requires=">=3.10",
)
