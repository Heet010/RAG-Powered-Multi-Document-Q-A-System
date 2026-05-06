import os
import streamlit as st
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger import log_event
from config import CHUNK_SIZE, CHUNK_OVERLAP

def save_uploaded_files(uploaded_files, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    saved_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(dest_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
    return saved_paths

def load_documents_langchain(dir_path: str) -> List[Document]:
    docs = []
    pdf_files = list(Path(dir_path).glob("*.pdf"))
    from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader
    
    for pdf_path in pdf_files:
        try:
            loader = PyMuPDFLoader(str(pdf_path))
            pages = loader.load()
            total_text = "".join([p.page_content for p in pages])
            
            if len(total_text.strip()) < 100:
                log_event(f"Low text content detected in {pdf_path.name}, using OCR mode...")
                loader = UnstructuredPDFLoader(str(pdf_path), mode="elements", strategy="hi_res")
                pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                length_function=len
            )
            chunks = text_splitter.split_documents(pages)
            log_event(f"Created {len(chunks)} chunks from {pdf_path.name}")
            
            for chunk in chunks:
                docs.append(Document(
                    page_content=chunk.page_content,
                    metadata={**chunk.metadata, "source": pdf_path.name}
                ))
        except Exception as e:
            st.error(f"Failed to load {pdf_path.name}: {e}")
            log_event(f"Error loading {pdf_path.name}: {e}", "ERROR")
    return docs