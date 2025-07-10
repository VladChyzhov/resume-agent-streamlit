import streamlit as st
import db

# Ensure shared data dict exists
if "data" not in st.session_state:
    st.session_state.data = {}

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("💼 Опыт работы")

# ---------- Input job experience ----------
st.subheader("Добавить место работы")

with st.form(key="exp_form", clear_on_submit=True):
    company = st.text_input("Компания")
    position = st.text_input("Должность")
    period = st.text_input("Период", placeholder="2021-2023")
    description = st.text_area("Описание обязанностей")
    submitted = st.form_submit_button("Добавить")
    if submitted and company and position:
        entry = {
            "company": company,
            "position": position,
            "period": period,
            "description": description,
        }
        st.session_state.data.setdefault("experience", []).append(entry)
        st.success("Запись добавлена")

# ---------- List current experiences ----------
exp_entries = st.session_state.data.get("experience", [])
if exp_entries:
    st.subheader("Опыт работы")
    for idx, e in enumerate(exp_entries, start=1):
        st.markdown(
            f"{idx}. **{e['company']}** — {e['position']} ({e['period']})  \n{e['description']}")

# ---------- Document upload ----------
st.divider()
st.subheader("Документы (рекомендации, грамоты)")
doc = st.file_uploader("Загрузите документ", key="exp_upload")
if st.button("Сохранить документ", key="exp_save") and doc:
    db.save_document(doc, st.session_state.user_id)
    st.success("Документ сохранён")

docs = db.list_documents(st.session_state.user_id)
if docs:
    st.write("### Загруженные документы")
    for _id, name in docs:
        st.write(f"{_id}. {name}")

# ---------- Navigation ----------
col1, col2 = st.columns([1,1])
with col1:
    if st.button("⬅️ Назад"):
        st.switch_page("pages/2_Education.py")
with col2:
    if st.button("Далее ➡️"):
        st.switch_page("pages/4_Skills_Languages.py")
