import streamlit as st

def apply_custom_css():
    """Applies the Yulu-style CSS to the Streamlit app."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }
        
        .main {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            background-attachment: fixed;
        }
        .block-container {
            background: rgba(17, 24, 39, 0.85);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
        }
        h1 {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 1rem;
            animation: fadeInDown 1s ease-in-out;
        }
        h2 { 
            color: #f3f4f6 !important; 
            border-bottom: 3px solid #8b5cf6; 
            padding-bottom: 0.5rem; 
            font-weight: 700 !important;
        }
        h3 { color: #e5e7eb !important; font-weight: 600 !important; }
        p, li, span, div { color: #cbd5e1; }
        
        .stTabs [data-baseweb="tab-list"] { 
            gap: 12px; 
            background-color: rgba(17, 24, 39, 0.5);
            padding: 0.5rem;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
            color: #a78bfa; 
            border-radius: 10px; 
            padding: 12px 24px; 
            font-weight: 600; 
            transition: all 0.3s ease; 
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        .stTabs [data-baseweb="tab"]:hover { 
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
            transform: translateY(-2px); 
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important; 
            color: white !important; 
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        }
        
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%); 
            border-right: 1px solid rgba(139, 92, 246, 0.3);
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { 
            color: white !important; 
            -webkit-text-fill-color: white !important; 
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
            color: white; 
            border-radius: 12px; 
            padding: 0.75rem 2rem; 
            font-weight: 600; 
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); 
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6); 
        }
        
        .card {
            padding: 1rem; 
            border-radius: 16px; 
            text-align: center; 
            color: white; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.4); 
            transition: all 0.4s ease; 
            border: 1px solid rgba(255,255,255,0.1);
        }
        .card:hover { 
            transform: translateY(-8px) scale(1.02); 
            box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
        }
        
        @keyframes fadeInDown { 
            from { opacity: 0; transform: translateY(-30px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        
        .stExpander {
            background: rgba(17, 24, 39, 0.5);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 12px;
        }
        
        /* Text Area Styling */
        .stTextArea textarea {
            background-color: rgba(17, 24, 39, 0.6) !important;
            color: #e5e7eb !important;
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
            border-radius: 12px !important;
        }
        .stTextArea textarea:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renders the top header and creator badge."""
    st.markdown("""
    <div style='position: fixed; top: 3.5rem; right: 1.5rem; z-index: 9999;'>
        <div style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
                    border-radius: 20px; padding: 0.6rem 1.2rem; 
                    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.5);'>
                <span style='color: white; font-weight: 700; font-size: 0.9rem; letter-spacing: 1.5px;'>
                &#10024; By heetkumar bhalani (AI enthusiast)
            </span>
        </div>
    </div>
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 style='font-size: 4rem; margin-bottom: 0;'>&#128218; Universal RAG Chatbot</h1>
        <p style='font-size: 1.3rem; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-top: 0.5rem;'>
            &#127919; AI-Powered Document Q&A System
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_how_to_use():
    """Renders the Quick Guide workflow UI."""
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 2rem;'>
        <h3 style='text-align: center; margin-top: 0; color: #a78bfa !important; font-size: 1.2rem;'>&#128640; Quick Guide</h3>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; text-align: center;'>
            <div style='flex: 1; min-width: 120px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>&#128194;</div>
                <div style='font-weight: 600; color: #fff;'>1. Upload PDF</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>Use sidebar/uploader</div>
            </div>
            <div style='font-size: 1.2rem; color: #666;'>➔</div>
            <div style='flex: 1; min-width: 120px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>&#9203;</div>
                <div style='font-weight: 600; color: #fff;'>2. Wait 20-30s</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>Processing docs</div>
            </div>
            <div style='font-size: 1.2rem; color: #666;'>➔</div>
            <div style='flex: 1; min-width: 120px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>&#128172;</div>
                <div style='font-weight: 600; color: #fff;'>3. Ask Question</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>In Chat tab</div>
            </div>
            <div style='font-size: 1.2rem; color: #666;'>➔</div>
            <div style='flex: 1; min-width: 120px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>&#129302;</div>
                <div style='font-weight: 600; color: #fff;'>4. Wait 20-30s</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>AI generating</div>
            </div>
            <div style='font-size: 1.2rem; color: #666;'>➔</div>
            <div style='flex: 1; min-width: 120px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>&#128218;</div>
                <div style='font-weight: 600; color: #fff;'>5. View Sources</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>Check citations</div>
            </div>
        </div>
        <div style='margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; color: #a78bfa;'>
            &#128161; <strong>Tip:</strong> If answers aren't found, click <strong>"&#128296; Rebuild Index"</strong> in sidebar & re-upload.
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)


def get_developer_notes():
    """Returns the Developer Notes HTML content."""
    return """
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;'>
        
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.3);'>
            <h4 style='color: #a78bfa !important; margin-top: 0;'>&#9889; Groq Integration</h4>
            <p style='font-size: 0.95rem;'>
                If you set <code>GROQ_API_KEY</code> in your environment, the app will automatically use Groq's high-speed inference via <code>langchain_groq</code>. 
                <br><br>
                <strong>Fallback:</strong> If Groq is unavailable, the app falls back to OpenAI (if configured) or handles the error gracefully. For production, ensure robust fallback logic is in place.
            </p>
        </div>

        <div style='background: rgba(236, 72, 153, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(236, 72, 153, 0.3);'>
            <h4 style='color: #f472b6 !important; margin-top: 0;'>&#128190; Index Persistence</h4>
            <p style='font-size: 0.95rem;'>
                The FAISS vector index is saved locally in the <code>faiss_index_storage</code> directory. This speeds up repeated runs by avoiding re-indexing.
                <br><br>
                <strong>Action:</strong> Use the <strong>"&#128296; Rebuild Index"</strong> button in the sidebar to force a fresh rebuild if your documents change.
            </p>
        </div>

        <div style='background: rgba(56, 239, 125, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(56, 239, 125, 0.3);'>
            <h4 style='color: #38ef7d !important; margin-top: 0;'>&#129504; Memory & Context</h4>
            <p style='font-size: 0.95rem;'>
                This implementation uses a simple <strong>session-state chat history</strong>. 
                <br><br>
                <strong>Customization:</strong> You can plug in LangChain's advanced memory classes (e.g., <code>ConversationBufferMemory</code>) to maintain longer context windows or persist chat history to a database (Redis, SQL) for production apps.
            </p>
        </div>

        <div style='background: rgba(251, 146, 60, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(251, 146, 60, 0.3);'>
            <h4 style='color: #fb923c !important; margin-top: 0;'>&#128737; Safety & Instructions</h4>
            <p style='font-size: 0.95rem;'>
                The LLM is strictly instructed to answer <strong>ONLY</strong> from the provided sources.
                <br><br>
                <strong>Advisory:</strong> Always review AI-generated outputs before using them in critical production environments. Hallucinations are reduced but possible.
            </p>
        </div>

        <div style='background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(96, 165, 250, 0.3); grid-column: 1 / -1;'>
            <h4 style='color: #60a5fa !important; margin-top: 0;'>&#128257; LlamaIndex Alternative</h4>
            <p style='font-size: 0.95rem;'>
                If you prefer <strong>LlamaIndex</strong>, this app can be adapted to build a <code>VectorStoreIndex</code> and use its <code>as_query_engine()</code> method. The architecture is modular, allowing you to swap the LangChain retrieval logic with LlamaIndex's powerful indexing capabilities easily.
            </p>
        </div>

    </div>
    """

def render_empty_state():
    """Renders the message shown when no PDFs are uploaded yet."""
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(139, 92, 246, 0.1); border-radius: 20px; border: 2px solid rgba(139, 92, 246, 0.3);'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>&#128193;</div>
        <h2 style='color: #a78bfa !important;'>Upload Your PDFs to Get Started</h2>
        <p style='font-size: 1.1rem; color: #cbd5e1;'>Use the file uploader above to upload one or more PDF files</p>
        <p style='color: #94a3b8;'>Limit: 200MB per file • Supports multiple PDFs</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Renders the bottom footer of the application."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Built By heetkumar bhalani (AI enthusiast)</p>
        <p>Universal RAG Chatbot • Built with LangChain, FAISS & Streamlit</p>
        <p>Powered by Gemini LLM & HuggingFace Embeddings</p>
    </div>
    """, unsafe_allow_html=True)