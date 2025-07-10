import streamlit as st
import db

st.set_page_config(page_title="Resume Builder - Login", page_icon="🔐", initial_sidebar_state="collapsed")

if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

# Hide sidebar only when not logged in
if st.session_state.get("user_id") is None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Show login and registration pages

def show_login():
    st.title("🔐 Login")
    st.markdown("Welcome to Resume Builder. Please login to continue.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    user_id = db.authenticate_user(username, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.error("Please enter both username and password.")
        
        with col_btn2:
            if st.button("Register", use_container_width=True):
                st.session_state.show_registration = True
                st.rerun()

def show_registration():
    st.title("📝 Registration")
    st.markdown("Create a new account to get started.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Username", key="reg_user", placeholder="Choose a username")
        password = st.text_input("Password", type="password", key="reg_pass", placeholder="Choose a strong password")
        password_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm", placeholder="Confirm your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Create Account", type="primary", use_container_width=True):
                if username and password:
                    if password != password_confirm:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        try:
                            user_id = db.register_user(username, password)
                            st.success("Account created successfully! Please login.")
                            st.session_state.show_registration = False
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
                else:
                    st.error("Please fill in all fields.")
        
        with col_btn2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state.show_registration = False
                st.rerun()

# Redirect if already logged in
if st.session_state.get("user_id"):
    st.switch_page("pages/1_Personal_Info.py")

# Show appropriate page
if st.session_state.get("show_registration"):
    show_registration()
else:
    show_login()
