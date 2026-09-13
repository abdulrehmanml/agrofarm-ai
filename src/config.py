import os
import streamlit as st
from pathlib import Path

# Base Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Data Paths
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIELD_STATUS_PATH = PROCESSED_DATA_DIR / "field_status.csv"

# Vector Store Paths
VECTORSTORE_PATH = DATA_DIR / "vectorstore" / "agri_vectorstore"
VECTORIZER_PATH = DATA_DIR / "vectorstore" / "tfidf_vectorizer.pkl"

# API Keys 
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
