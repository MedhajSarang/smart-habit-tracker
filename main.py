import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Habit Tracker", page_icon="📊", layout="centered")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Login", "Dashboard", "Add Habit"])

# --- PAGE ROUTING ---
if page == "Login":
    st.title("🔐 Login")
    st.write("Login functionality coming soon...")
    # We will eventually import a login function here

elif page == "Dashboard":
    st.title("📊 Your Progress")
    st.write("Visualizations will appear here.")
    # We will eventually put our Plotly graphs here

elif page == "Add Habit":
    st.title("➕ Track a New Habit")
    st.write("Form to add habits will appear here.")

# --- TEMP: DATABASE CHECK ---
from database.db_connection import get_db_connection

if st.sidebar.button("Test DB Connection"):
    db = get_db_connection()
    if db:
        st.sidebar.success("✅ Connected to Database!")