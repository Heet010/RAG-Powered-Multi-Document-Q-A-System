import logging
import datetime
import streamlit as st

# Logging Setup
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_event(message: str, level: str = "INFO"):
    """Log event to file and session state"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
        
    if "app_logs" not in st.session_state:
        st.session_state["app_logs"] = []
    
    emoji = '&#128308;' if level=='ERROR' else ('&#9888;' if level=='WARNING' else '&#128313;')
    st.session_state["app_logs"].insert(0, f"{emoji} {log_entry}")
    
    if len(st.session_state["app_logs"]) > 100:
        st.session_state["app_logs"] = st.session_state["app_logs"][:100]