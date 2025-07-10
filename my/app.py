import streamlit as st

st.set_page_config(
    page_title="Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded" if "user_id" in st.session_state and st.session_state.user_id else "collapsed"
)

# Shared session initialization
if "data" not in st.session_state:
    st.session_state.data = {}
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

# Sidebar for logged-in users
if st.session_state.user_id is not None:
    with st.sidebar:
        st.title("📄 Resume Builder")
        st.markdown("---")
        
        # Navigation links
        st.page_link("pages/1_Personal_Info.py", label="👤 Personal Info", icon="👤")
        st.page_link("pages/2_Education.py", label="🎓 Education", icon="🎓")
        st.page_link("pages/3_Work_Experience.py", label="💼 Work Experience", icon="💼")
        st.page_link("pages/4_Skills_Languages.py", label="🛠️ Skills & Languages", icon="🛠️")
        st.page_link("pages/5_Generate_Resume.py", label="📄 Generate Resume", icon="📄")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.data = {}
            st.rerun()

# Redirect based on auth state
if st.session_state.user_id is None:
    st.switch_page("pages/0_Auth.py")
else:
    st.switch_page("pages/1_Personal_Info.py")
