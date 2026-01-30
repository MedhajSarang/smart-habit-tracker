import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Habit Tracker", page_icon="📊", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")

# Dynamic Menu: Show different options if logged in
if st.session_state.user_id:
    st.sidebar.write(f"👤 **{st.session_state.username}**")
    page = st.sidebar.radio("Go to:", ["Dashboard", "Add Habit"])
    
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
else:
    page = "Login" # Force them to stay on Login page

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
        username_in = st.text_input("Username", key="login_user")
        password_in = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            from database.queries import verify_login
            user_id = verify_login(username_in, password_in)
            
            if user_id:
                # SAVE TO SESSION STATE (The Backpack)
                st.session_state.user_id = user_id
                st.session_state.username = username_in
                st.success(f"Welcome back, {username_in}!")
                st.rerun() # Refresh the app to update the state
            else:
                st.error("Incorrect username or password.")

elif page == "Dashboard":
    st.title("📊 Your Progress")
    st.write("Visualizations will appear here.")
    # We will eventually put our Plotly graphs here

elif page == "Add Habit":
    st.title("➕ Add a New Habit")
    st.write("What do you want to track?")
    
    with st.form("add_habit_form"):
        habit_name = st.text_input("Habit Name (e.g., Drink 2L Water)")
        
        # Two columns for better layout
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Health", "Career", "Learning", "Mindfulness", "Other"])
        with col2:
            frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Weekdays"])
            
        submit = st.form_submit_button("Create Habit")
        
        if submit:
            if habit_name:
                from database.queries import add_habit
                # usage of session_state.user_id ensures we link it to the logged-in person
                result = add_habit(st.session_state.user_id, habit_name, category, frequency)
                
                if result == "Success":
                    st.success(f"✅ Habit '{habit_name}' added successfully!")
                else:
                    st.error(f"❌ Error: {result}")
            else:
                st.warning("⚠️ Please enter a habit name.")

# --- TEMP: DATABASE CHECK ---
from database.db_connection import get_db_connection

if st.sidebar.button("Test DB Connection"):
    db = get_db_connection()
    if db:
        st.sidebar.success("✅ Connected to Database!")