import streamlit as st
import tempfile
import os
import html
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Custom Module Imports ---
from config import (
    INDEX_DIR, TOP_K, GROQ_AVAILABLE, OPENAI_AVAILABLE, 
    GROQ_MODELS, GEMINI_AVAILABLE, get_api_keys
)
from logger import log_event
from ui_components import (
    apply_custom_css, render_header, render_how_to_use, 
    get_developer_notes, render_empty_state, render_footer
)
from document_service import save_uploaded_files, load_documents_langchain
from rag_service import build_or_load_faiss, get_llm_instance, process_query

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Universal RAG Chatbot",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()
render_header()
render_how_to_use()

# ==========================================
# 2. SIDEBAR CONFIGURATION
# ==========================================
has_groq, has_openai, has_gemini, groq_key, openai_key, gemini_key = get_api_keys()

with st.sidebar:
    st.markdown("## &#9881; Settings")
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.3);'>
        <h3 style='color: #a78bfa !important; margin-top: 0;'>&#128202; Configuration</h3>
        <p><strong>Embedding:</strong> all-mpnet-base-v2</p>
        <p><strong>Chunk Size:</strong> 800</p>
        <p><strong>Top-K:</strong> 10</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    use_groq = st.checkbox("Prefer Groq LLM", value=False)
    force_rebuild = st.button("&#128296; Rebuild Index", help="Force rebuild FAISS index")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(56, 239, 125, 0.3);'>
        <h3 style='color: #38ef7d !important; margin-top: 0;'>&#8505; Status</h3>
        <p>{'&#9989;' if GEMINI_AVAILABLE and has_gemini else '&#10060;'} Gemini</p>
        <p>{'&#9989;' if GROQ_AVAILABLE and has_groq else '&#10060;'} Groq</p>
        <p>{'&#9989;' if OPENAI_AVAILABLE and has_openai else '&#10060;'} OpenAI</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download Chat History Logic
    if "messages" in st.session_state and st.session_state["messages"]:
        chat_history_text = f"Chat History - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_history_text += "="*50 + "\n\n"
        
        for role, content in st.session_state["messages"]:
            clean_content = content.replace("<b>", "**").replace("</b>", "**")
            if "|||DEBUG_CHUNKS" in clean_content:
                clean_content = clean_content.split("|||DEBUG_CHUNKS")[0]
            if "|||FOOTER" in clean_content:
                clean_content = clean_content.split("|||FOOTER")[0]
                
            chat_history_text += f"[{role.upper()}]:\n{clean_content.strip()}\n\n{'-'*50}\n\n"
            
        st.download_button(
            label="&#128190; Download Chat History",
            data=chat_history_text,
            file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# ==========================================
# 3. MAIN UI & FILE UPLOAD
# ==========================================
st.header("&#128193; Upload PDFs")
uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    accept_multiple_files=True,
    type=["pdf"],
    help="Upload PDF documents to create your knowledge base"
)

tab1, tab2, tab3, tab4 = st.tabs(["&#128172; Chat", "&#8505; Info & Tech Stack", "&#128220; Logs", "&#128221; Notes"])

# --- TAB 4: DEVELOPER NOTES ---
with tab4:
    st.markdown("### &#128221; Developer Notes & Customization")
    st.html(get_developer_notes())

# --- TAB 2: INFO & TECH STACK ---
with tab2:
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("### &#9889; Features")
        st.markdown("""
        - &#128196; **Multi-PDF Support** - Upload multiple documents
        - &#128269; **Semantic Search** - FAISS vector similarity
        - &#129302; **Multiple LLM Options** - Groq (fast) or OpenAI
        - &#128218; **Source Citations** - See where answers come from
        - &#128190; **Persistent Index** - Faster subsequent queries
        - &#128259; **Auto Fallback** - Switches models if one fails
        """)
    with col_info2:
        st.markdown("### &#128736; Tech Stack")
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.3);'>
            <p><strong>Frontend:</strong> Streamlit</p>
            <p><strong>Orchestration:</strong> LangChain</p>
            <p><strong>Vector DB:</strong> FAISS</p>
            <p><strong>Embeddings:</strong> HuggingFace (all-mpnet-base-v2)</p>
            <p><strong>LLM:</strong> Gemini & Groq (when configured)</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: LOGS ---
with tab3:
    st.markdown("### &#128220; Application Logs")
    if st.button("&#128259; Refresh Logs"):
        st.rerun()
    
    log_content = ""
    try:
        if os.path.exists('app.log'):
            with open('app.log', 'r') as f:
                log_content = f.read()
    except Exception:
        pass

    if not log_content and "app_logs" in st.session_state:
        log_content = "\n".join(st.session_state["app_logs"])
        
    st.text_area("Live Logs", value=log_content, height=400, disabled=True)

# --- TAB 1: CORE CHAT & RAG LOGIC ---
with tab1:
    if uploaded_files:
        temp_dir = tempfile.mkdtemp(prefix="rag_chatbot_")
        
        try:
            # 1. Process Documents (Only if new)
            if "processed_files" not in st.session_state or st.session_state.get("processed_files") != [f.name for f in uploaded_files]:
                log_event(f"Processing {len(uploaded_files)} uploaded files")
                saved_paths = save_uploaded_files(uploaded_files, temp_dir)
                st.success(f"&#9989; Uploaded {len(saved_paths)} file(s)")
                
                with st.spinner("&#128214; Loading and chunking documents..."):
                    docs = load_documents_langchain(temp_dir)
                    if not docs:
                        st.error("&#10060; No documents loaded")
                        st.stop()
                    st.info(f"&#128196; Loaded {len(docs)} document chunks")
                
                # Build FAISS Index
                db = build_or_load_faiss(docs, INDEX_DIR, force_rebuild)
                st.session_state["retriever"] = db.as_retriever(search_kwargs={"k": TOP_K})
                st.session_state["processed_files"] = [f.name for f in uploaded_files]

            # 2. Setup Chat Interface
            if "retriever" in st.session_state:
                st.markdown("### &#128172; Chat with Your Documents")
                
                if "messages" not in st.session_state:
                    st.session_state["messages"] = []
                
                # Render Chat History
                for role, message in st.session_state["messages"]:
                    if role == "user":
                        st.markdown(f"""
                        <div style='display: flex; gap: 12px; margin-bottom: 1rem;'>
                            <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #FF0099 0%, #493240 100%); display: flex; align-items: center; justify-content: center; font-size: 20px;'>&#128100;</div>
                            <div style='flex: 1; padding: 16px 22px; border-radius: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
                                {html.escape(message)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Extract UI formatting (Sources & Footer) from assistant message
                        parts = message.split("**&#128218; Sources:**")
                        main_answer = parts[0].strip()
                        
                        st.markdown(f"""
                        <div style='display: flex; gap: 12px; margin-bottom: 1rem;'>
                            <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #00F260 0%, #0575E6 100%); display: flex; align-items: center; justify-content: center; font-size: 20px;'>&#129302;</div>
                            <div style='flex: 1; padding: 16px 22px; border-radius: 20px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e0e0e0;'>
                                {html.escape(main_answer).replace(chr(10), '<br>')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Render Sources if available
                        if len(parts) > 1:
                            sources_raw = parts[1].split("|||")[0].strip().split("\n")
                            with st.expander("&#128218; View Sources", expanded=False):
                                for line in sources_raw:
                                    if line.startswith("**["):
                                        st.markdown(f"**{line.replace('**', '')}**")
                                    elif line.startswith(">"):
                                        st.markdown(f"> {line[1:].strip()}")
                
                # Chat Input
                def submit_query():
                    if st.session_state.get("query_input"):
                        st.session_state["messages"].append(("user", st.session_state["query_input"]))
                        st.session_state["query_input"] = ""

                st.text_area("Ask a question about your documents...", key="query_input")
                
                col_actions1, col_actions2 = st.columns(2)
                with col_actions1:
                    st.button("&#10140; Enter Query", on_click=submit_query, use_container_width=True)
                with col_actions2:
                    if st.button("&#128465; Clear Conversation", use_container_width=True):
                        st.session_state["messages"] = []
                        st.rerun()

                # Process New Query
                if st.session_state["messages"] and st.session_state["messages"][-1][0] == "user":
                    with st.spinner("&#129504; Thinking..."):
                        latest_query = st.session_state["messages"][-1][1]

                        provider_order = []
                        if has_gemini and gemini_key:
                            provider_order.append(("gemini", "gemini-2.5-flash", gemini_key))
                        if GROQ_AVAILABLE and groq_key:
                            provider_order.append(("groq", GROQ_MODELS[0], groq_key))
                        if use_groq and GROQ_AVAILABLE and groq_key:
                            provider_order = [("groq", GROQ_MODELS[0], groq_key)] + [item for item in provider_order if item[0] != "groq"]

                        if not provider_order:
                            st.error("&#10060; No API key configured for Gemini, Groq, or OpenAI.")
                            st.stop()

                        last_error = None
                        for current_provider, current_model, current_key in provider_order:
                            try:
                                llm = get_llm_instance(current_key, current_model, current_provider)
                                result = process_query(latest_query, st.session_state["retriever"], llm)
                            
                                answer = result.get("answer", "No answer generated")
                                source_docs = result.get("context", [])
                            
                                # Format Response with Sources
                                full_answer = answer
                                if source_docs:
                                    full_answer += "\n\n**&#128218; Sources:**\n"
                                    for i, doc in enumerate(source_docs, 1):
                                        source = doc.metadata.get("source", f"Document {i}")
                                        snippet = " ".join(doc.page_content[:200].split()) + "..."
                                        full_answer += f"\n**[{i}]** {source}\n> {snippet}\n"
                                        
                                full_answer += f"|||FOOTER:Generated with: {current_provider}:{current_model}"
                            
                                st.session_state["messages"].append(("assistant", full_answer))
                                st.rerun()
                            
                            except Exception as e:
                                last_error = e
                                log_event(f"Provider {current_provider} failed: {str(e)}", "WARNING")
                                continue

                        if last_error:
                            st.error(f"Error generating response: {str(last_error)}")
                            log_event(f"Query Error: {str(last_error)}", "ERROR")
                            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            log_event(f"App error: {e}", "ERROR")

    else:
        render_empty_state()

# ==========================================
# 4. FOOTER
# ==========================================
render_footer()