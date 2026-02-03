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
    page = st.sidebar.radio("Go to:", ["Dashboard", "Analytics", "Add Habit", "Manage Habits"])
    
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
    st.title("📊 Your Daily Dashboard")
    
    # 1. Get the Current Date
    from datetime import date
    today = date.today()
    st.write(f"**Date:** {today.strftime('%B %d, %Y')}")
    st.divider()
    
    # 2. Fetch User's Habits
    from database.queries import get_user_habits, is_habit_done_today, toggle_habit
    habits = get_user_habits(st.session_state.user_id, active_only=True)
    
    if not habits:
        st.info("You haven't added any habits yet. Go to 'Add Habit' to start!")
    else:
        # 3. Display Habits as Checkboxes
        st.subheader("Today's Tasks")
        
        for habit in habits:
            habit_id = habit['habit_id']
            habit_name = habit['name']
            
            # Check DB to see if it was already done today
            is_done = is_habit_done_today(habit_id, today)
            
            # Create a checkbox
            # value=is_done sets the initial state (checked/unchecked)
            checked = st.checkbox(f"**{habit_name}** ({habit['category']})", value=is_done, key=habit_id)
            
            # 4. Handle Logic (Only if state changed)
            if checked != is_done:
                toggle_habit(habit_id, today, checked)
                st.rerun() # Refresh to confirm the save

elif page == "Analytics":
    st.title("📈 Analytics Dashboard")
    
    from utils.analytics import get_habit_stats
    import plotly.express as px
    
    # 1. Get the Data
    df = get_habit_stats(st.session_state.user_id)
    
    if df.empty:
        st.info("No data available yet. Complete some habits!")
    else:
        # 2. Plotly Bar Chart
        st.subheader("🏆 Consistency Score")
        
        # This creates a beautiful interactive bar chart
        fig = px.bar(
            df, 
            x="name", 
            y="count", 
            color="category",
            text="count",
            template="plotly_dark", # Dark mode style
            labels={"count": "Days Completed", "name": "Habit"}
        )
        # Display it
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        
        # 3. Heatmap (Day vs Habit)
        st.subheader("🔥 Consistency Heatmap")
        st.write("When are you most active?")
        
        from utils.analytics import get_day_of_week_stats
        df_heatmap = get_day_of_week_stats(st.session_state.user_id)
        
        if not df_heatmap.empty:
            fig2 = px.density_heatmap(
                df_heatmap,
                x="day_name",
                y="name",
                z="count",
                text_auto=True, # Shows the numbers in the boxes
                color_continuous_scale="Greens", # GitHub style colors
                labels={"day_name": "Day", "name": "Habit", "count": "Completions"}
            )
            st.plotly_chart(fig2, use_container_width=True)

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

elif page == "Manage Habits":
    st.title("⚙️ Manage Your Habits")
    
    from database.queries import get_user_habits, delete_habit, update_habit, toggle_habit_status
    
    # 1. Fetch current habits
    habits = get_user_habits(st.session_state.user_id, active_only=False)
    
    if not habits:
        st.info("You have no habits to manage.")
    else:
        for habit in habits:
            # Visual Cue: Add (Archived) to the name if it's inactive
            status_icon = "🟢" if habit['is_active'] else "zzz"
            expander_title = f"{status_icon} {habit['name']}"
            
            with st.expander(expander_title):
                st.write(f"**Current Status:** {'Active' if habit['is_active'] else 'Archived'}")
                
                # --- EDIT SECTION (Same as before) ---
                st.subheader("Edit Details")
                with st.form(key=f"edit_{habit['habit_id']}"):
                    new_name = st.text_input("Name", value=habit['name'])
                    # ... (Keep your existing selectboxes for Category/Frequency here) ...
                    # To save time, just copy the col1/col2 logic from your previous code
                    col1, col2 = st.columns(2)
                    new_cat = col1.selectbox("Category", ["Health", "Career", "Learning", "Mindfulness", "Other"], index=["Health", "Career", "Learning", "Mindfulness", "Other"].index(habit['category']))
                    new_freq = col2.selectbox("Frequency", ["Daily", "Weekly", "Weekdays"], index=["Daily", "Weekly", "Weekdays"].index(habit['frequency']))
                    
                    if st.form_submit_button("Save Changes"):
                        update_habit(habit['habit_id'], new_name, new_cat, new_freq)
                        st.rerun()

                st.divider()

                # --- ACTIONS SECTION ---
                col_a, col_b = st.columns(2)
                
                # 1. ARCHIVE / ACTIVATE BUTTON
                with col_a:
                    btn_label = "Deactivate (Archive)" if habit['is_active'] else "Reactivate"
                    if st.button(btn_label, key=f"arch_{habit['habit_id']}"):
                        toggle_habit_status(habit['habit_id'], habit['is_active'])
                        st.rerun()
                
                # 2. HARD DELETE BUTTON (Still good to keep for mistakes)
                with col_b:
                    if st.button("🗑️ Delete Permanently", key=f"del_{habit['habit_id']}"):
                        delete_habit(habit['habit_id'])
                        st.rerun()

# --- TEMP: DATABASE CHECK ---
from database.db_connection import get_db_connection

if st.sidebar.button("Test DB Connection"):
    db = get_db_connection()
    if db:
        st.sidebar.success("✅ Connected to Database!")