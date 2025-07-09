# app.py – минимально рабочий Streamlit‑интерфейс (без падений)
# -------------------------------------------------------------
# На этом этапе показываем страницы‑заглушки, чтобы убедиться, что
# код компилируется и приложение запускается. После проверки можно
# постепенно добавлять логику загрузки файлов, голосового ввода и
# вызовы FastAPI‑эндпойнтов.
# -------------------------------------------------------------

import streamlit as st
import requests
import db

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

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "show_registration" not in st.session_state:
    st.session_state.show_registration = False


def show_login():
    st.title("Вход")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        user_id = db.authenticate_user(username, password)
        if user_id:
            st.session_state.user_id = user_id
            st.experimental_rerun()
        else:
            st.error("Неверные учётные данные")
    if st.button("Регистрация"):
        st.session_state.show_registration = True
        st.experimental_rerun()


def show_registration():
    st.title("Регистрация")
    username = st.text_input("Логин", key="reg_user")
    password = st.text_input("Пароль", type="password", key="reg_pass")
    if st.button("Создать аккаунт"):
        try:
            user_id = db.register_user(username, password)
            st.success("Аккаунт создан. Войдите.")
            st.session_state.show_registration = False
            st.experimental_rerun()
        except ValueError as e:
            st.error(str(e))
    if st.button("Назад"):
        st.session_state.show_registration = False
        st.experimental_rerun()


if st.session_state.user_id is None:
    if st.session_state.show_registration:
        show_registration()
    else:
        show_login()
    st.stop()

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

    saved = db.load_personal_info(st.session_state.user_id)
    default_name = saved[0] if saved else ""
    default_email = saved[1] if saved else ""
    default_phone = saved[2] if saved else ""
    saved_photo = saved[3] if saved else None

    st.session_state.data.update({"name": default_name, "email": default_email, "phone": default_phone})

    name = st.text_input("Имя и фамилия", default_name)
    email = st.text_input("Email", default_email)
    phone = st.text_input("Телефон", default_phone)
    photo = st.file_uploader("Фото (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if saved_photo and not photo:
        st.image(saved_photo, caption="Сохранённое фото")

    if st.button("Сохранить"):
        photo_bytes = photo.read() if photo else saved_photo
        db.save_personal_info(st.session_state.user_id, name, email, phone, photo_bytes)
        st.session_state.data.update({"name": name, "email": email, "phone": phone})
        st.success("Сохранено! Перейдите к вкладке 'Образование'.")

# ----------------------------------------
# 2. Образование (заглушка)
# ----------------------------------------

elif page == "Образование":
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

# ----------------------------------------
# 3. Опыт работы (заглушка)
# ----------------------------------------

elif page == "Опыт работы":
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
