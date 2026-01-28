import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Habit Tracker", page_icon="📊", layout="centered")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Login", "Dashboard", "Add Habit"])

# --- PAGE ROUTING ---
if page == "Login":
    st.title("🔐 Login / Sign Up")
    
    # Create tabs to switch between Login and Register
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # --- SIGN UP TAB ---
    with tab2:
        st.header("Create an Account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        
        if st.button("Sign Up"):
            if new_user and new_pass:
                # Call our new function
                from database.queries import create_user
                result = create_user(new_user, new_pass)
                
                if result == "Success":
                    st.success("Account created! You can now login.")
                else:
                    st.error(f"Could not create account: {result}")
            else:
                st.warning("Please fill in both fields.")

    # --- LOGIN TAB ---
    with tab1:
        st.header("Welcome Back")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.info("Login logic coming next...")

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