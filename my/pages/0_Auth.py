import streamlit as st
import db

st.set_page_config(initial_sidebar_state="collapsed")

if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

if st.session_state.get("user_id") is None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# show login and registration pages

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

if st.session_state.get("user_id"):
    st.switch_page("pages/1_Personal_Info.py")

if st.session_state.get("show_registration"):
    show_registration()
else:
    show_login()
