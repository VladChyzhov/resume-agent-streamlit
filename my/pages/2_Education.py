import streamlit as st
import db

# Ensure shared data dict exists
if "data" not in st.session_state:
    st.session_state.data = {}

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🎓 Образование, дипломы, сертификаты")

doc = st.file_uploader("Загрузите документ", key="edu_upload")
if st.button("Сохранить документ", key="edu_save") and doc:
    db.save_document(doc, st.session_state.user_id)
    st.success("Документ сохранён")

docs = db.list_documents(st.session_state.user_id)
if docs:
    st.subheader("Загруженные документы")
    for _id, name in docs:
        st.write(f"{_id}. {name}")
