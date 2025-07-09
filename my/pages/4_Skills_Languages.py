import streamlit as st

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🛠️ Навыки и 🌍 Языки")
st.info("Здесь будет голосовой ввод навыков и языков.")
