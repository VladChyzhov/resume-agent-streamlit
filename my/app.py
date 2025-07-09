import streamlit as st

# Shared session initialization
if "data" not in st.session_state:
    st.session_state.data = {}
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

# Redirect based on auth state
if st.session_state.user_id is None:
    st.switch_page("pages/0_Auth.py")
else:
    st.switch_page("pages/1_Personal_Info.py")
