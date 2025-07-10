import streamlit as st

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🛠️ Навыки и 🌍 Языки")
st.info("Введите ваши ключевые навыки и языки. Вы можете перечислить через запятую или добавить построчно.")

# Ensure shared data dict exists
if "data" not in st.session_state:
    st.session_state.data = {}

# ----- Skills -----
st.subheader("Навыки")
skills_input = st.text_area(
    "Перечислите ваши навыки (каждый навык на новой строке или через запятую)",
    value="\n".join(st.session_state.data.get("skills", [])),
    placeholder="Python, SQL, Data Analysis, ...",
)

# ----- Languages -----
st.subheader("Языки")
langs_input = st.text_area(
    "Перечислите языки и уровень владения (каждый язык на новой строке или через запятую)",
    value="\n".join(st.session_state.data.get("languages", [])),
    placeholder="Русский – родной, Английский – B2, ...",
)

if st.button("Сохранить навыки и языки"):
    # Normalize by splitting on newlines and commas
    def _normalize(txt: str):
        parts = [p.strip() for ln in txt.split("\n") for p in ln.split(",")]
        return [p for p in parts if p]

    skills_list = _normalize(skills_input)
    lang_list = _normalize(langs_input)

    st.session_state.data.update({"skills": skills_list, "languages": lang_list})
    st.success("Сохранено! Перейдите к шагу 'Генерация резюме'.")
