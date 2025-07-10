import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("👤 Персональные данные")

# Load existing data
saved = db.load_personal_info(st.session_state.user_id)
default_name = saved[0] if saved and saved[0] else ""
default_email = saved[1] if saved and saved[1] else ""
default_phone = saved[2] if saved and saved[2] else ""
saved_photo = saved[3] if saved and len(saved) > 3 and saved[3] else None

# Update session state with defaults
st.session_state.data.update({"name": default_name, "email": default_email, "phone": default_phone})

# Form inputs with validation
name = st.text_input("Имя и фамилия", value=default_name, help="Введите ваше полное имя")
email = st.text_input("Email", value=default_email, help="Введите ваш email адрес")
phone = st.text_input("Телефон", value=default_phone, help="Введите ваш номер телефона")
photo = st.file_uploader("Фото (JPG/PNG)", type=["jpg", "jpeg", "png"], help="Загрузите ваше фото")

# Show existing photo if available
if saved_photo and not photo:
    st.image(saved_photo, caption="Сохранённое фото", width=200)

# Validation and save
if st.button("Сохранить"):
    # Input validation
    errors = []
    if not name.strip():
        errors.append("Имя и фамилия обязательны для заполнения")
    if email and "@" not in email:
        errors.append("Введите корректный email адрес")
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        # Handle photo bytes safely
        photo_bytes = None
        if photo:
            photo_bytes = photo.read()
        elif saved_photo:
            photo_bytes = saved_photo
        
        # Save to database
        try:
            db.save_personal_info(st.session_state.user_id, name.strip(), email.strip(), phone.strip(), photo_bytes)
            st.session_state.data.update({"name": name.strip(), "email": email.strip(), "phone": phone.strip()})
            st.success("Данные успешно сохранены! Перейдите к вкладке 'Образование'.")
        except Exception as e:
            st.error(f"Ошибка при сохранении данных: {str(e)}")

# Navigation help
st.info("💡 После сохранения данных перейдите к следующему шагу в боковой панели.")
