import streamlit as st
import sys, pathlib

# Allow importing from parent directory (project root) to access resume_pdf module
PARENT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from resume_pdf import generate_resume

# Ensure shared data dict exists
if "data" not in st.session_state:
    st.session_state.data = {}

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("📄 Генерация резюме")
data = st.session_state.get("data", {})

st.write("Черновые данные, собранные на предыдущих шагах:")
st.json(data)

if st.button("Сгенерировать PDF резюме"):
    if not data.get("name"):
        st.error("Необходимо заполнить как минимум персональные данные.")
    else:
        pdf_bytes = generate_resume(data)
        st.success("PDF резюме сгенерировано!")
        st.download_button(
            label="📥 Скачать резюме (PDF)",
            data=pdf_bytes,
            file_name="resume.pdf",
            mime="application/pdf",
        )
