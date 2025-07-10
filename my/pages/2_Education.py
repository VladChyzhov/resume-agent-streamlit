import streamlit as st
import db

# Ensure shared data dict exists
if "data" not in st.session_state:
    st.session_state.data = {}

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🎓 Образование, дипломы, сертификаты")

# ---------- Input basic education details ----------
st.subheader("Добавить запись об образовании")

with st.form(key="edu_form", clear_on_submit=True):
    institution = st.text_input("Учебное заведение")
    degree = st.text_input("Специальность / Степень")
    years = st.text_input("Годы обучения", placeholder="2018-2022")
    submitted = st.form_submit_button("Добавить")
    if submitted and institution and degree:
        entry = {
            "institution": institution,
            "degree": degree,
            "years": years,
        }
        st.session_state.data.setdefault("education", []).append(entry)
        st.success("Запись добавлена")

# ---------- List current entries ----------
edu_entries = st.session_state.data.get("education", [])
if edu_entries:
    st.subheader("Ваше образование")
    for idx, e in enumerate(edu_entries, start=1):
        st.write(f"{idx}. {e['institution']} — {e['degree']} ({e['years']})")

# ---------- Document upload ----------
st.divider()
st.subheader("Документы (дипломы, сертификаты)")
doc = st.file_uploader("Загрузите документ", key="edu_upload")
if st.button("Сохранить документ", key="edu_save") and doc:
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
        st.switch_page("pages/1_Personal_Info.py")
with col2:
    if st.button("Далее ➡️"):
        st.switch_page("pages/3_Work_Experience.py")
