import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. Load environment variables from .env file (if present)
load_dotenv()

def get_db_connection() -> Client:
    """
    Creates a Supabase client.
    Tries to load credentials from .env first (Backend mode).
    Falls back to st.secrets if .env is missing (Frontend mode).
    """
    # Try getting from standard environment variables (Backend/FastAPI)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    # If not found, try Streamlit secrets (Frontend/Streamlit)
    if not url or not key:
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        except FileNotFoundError:
            raise ValueError("❌ SUPABASE_URL and SUPABASE_KEY not found in .env or secrets.toml")

    return create_client(url, key)