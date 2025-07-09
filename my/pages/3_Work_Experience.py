import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("💼 Опыт работы")

doc = st.file_uploader("Загрузите документ", key="exp_upload")
if st.button("Сохранить документ", key="exp_save") and doc:
    db.save_document(doc, st.session_state.user_id)
    st.success("Документ сохранён")

docs = db.list_documents(st.session_state.user_id)
if docs:
    st.subheader("Загруженные документы")
    for _id, name in docs:
        st.write(f"{_id}. {name}")
