# app.py – минимально рабочий Streamlit‑интерфейс (без падений)
# -------------------------------------------------------------
# На этом этапе показываем страницы‑заглушки, чтобы убедиться, что
# код компилируется и приложение запускается. После проверки можно
# постепенно добавлять логику загрузки файлов, голосового ввода и
# вызовы FastAPI‑эндпойнтов.
# -------------------------------------------------------------

import streamlit as st
import requests
from db import save_document, list_documents

BACKEND_URL = "http://localhost:8000"  # пока не используется

# ----------------------------------------
# Вспомогательная функция (заготовка)
# ----------------------------------------

def post(endpoint: str, data=None, files=None):
    """Отправка POST‑запроса к backend. Сейчас не критично."""
    try:
        res = requests.post(f"{BACKEND_URL}{endpoint}", data=data, files=files, timeout=30)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Ошибка backend: {e}")
        return None

# ----------------------------------------
# Инициализация session_state
# ----------------------------------------

if "data" not in st.session_state:
    st.session_state.data = {}

# ----------------------------------------
# Навигация (sidebar)
# ----------------------------------------

page = st.sidebar.radio(
    "Разделы анкеты", [
        "Персональные данные",
        "Образование",
        "Опыт работы",
        "Навыки и языки",
        "Генерация резюме",
    ]
)

# ----------------------------------------
# 1. Персональные данные
# ----------------------------------------

if page == "Персональные данные":
    st.title("👤 Персональные данные")

    name = st.text_input("Имя и фамилия", st.session_state.data.get("name", ""))
    email = st.text_input("Email", st.session_state.data.get("email", ""))
    phone = st.text_input("Телефон", st.session_state.data.get("phone", ""))
    photo = st.file_uploader("Фото (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if st.button("Сохранить"):
        st.session_state.data.update({"name": name, "email": email, "phone": phone})
        if photo:
            st.session_state.data["photo"] = photo
        st.success("Сохранено! Перейдите к вкладке 'Образование'.")

# ----------------------------------------
# 2. Образование (заглушка)
# ----------------------------------------

elif page == "Образование":
    st.title("🎓 Образование, дипломы, сертификаты")
    diploma = st.file_uploader("Загрузите документ", type=["pdf", "jpg", "jpeg", "png"])
    if diploma:
        save_document(diploma)
        st.success("Файл сохранён")

    docs = list_documents()
    if docs:
        st.subheader("Сохранённые документы")
        for _id, name in docs:
            st.write(f"{_id}: {name}")

# ----------------------------------------
# 3. Опыт работы (заглушка)
# ----------------------------------------

elif page == "Опыт работы":
    st.title("💼 Опыт работы")
    resume_file = st.file_uploader("Загрузите документ", type=["pdf", "jpg", "jpeg", "png"])
    if resume_file:
        save_document(resume_file)
        st.success("Файл сохранён")

    docs = list_documents()
    if docs:
        st.subheader("Сохранённые документы")
        for _id, name in docs:
            st.write(f"{_id}: {name}")

# ----------------------------------------
# 4. Навыки и языки (заглушка)
# ----------------------------------------

elif page == "Навыки и языки":
    st.title("🛠️ Навыки и 🌍 Языки")
    st.info("Здесь будет голосовой ввод навыков и языков.")

# ----------------------------------------
# 5. Генерация резюме (заглушка)
# ----------------------------------------

elif page == "Генерация резюме":
    st.title("📄 Генерация резюме")
    st.write("Черновые данные, собранные на предыдущих шагах:")
    st.json(st.session_state.data)
    st.warning("Backend для генерации PDF ещё не подключён.")
