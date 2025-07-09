import streamlit as st

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("📄 Генерация резюме")
st.write("Черновые данные, собранные на предыдущих шагах:")
st.json(st.session_state.get("data", {}))
st.warning("Backend для генерации PDF ещё не подключён.")
