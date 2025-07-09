import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

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
