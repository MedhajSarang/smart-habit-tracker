import streamlit as st
from supabase import create_client, Client

# Initialize connection using the secrets we just saved
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

def get_db_connection():
    """Returns the Supabase client."""
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"❌ Could not connect to Supabase: {e}")
        return None