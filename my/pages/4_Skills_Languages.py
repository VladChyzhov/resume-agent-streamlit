import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🛠️ Навыки и 🌍 Языки")

# Create two columns for skills and languages
col1, col2 = st.columns(2)

with col1:
    st.subheader("💻 Технические навыки")
    
    # Add new skill form
    with st.expander("➕ Добавить навык", expanded=False):
        skill_name = st.text_input("Название навыка", key="skill_name", help="Например: Python, JavaScript, Photoshop")
        skill_level = st.selectbox("Уровень владения", 
                                 ["beginner", "intermediate", "advanced", "expert"], 
                                 key="skill_level",
                                 format_func=lambda x: {
                                     "beginner": "Начинающий",
                                     "intermediate": "Средний", 
                                     "advanced": "Продвинутый",
                                     "expert": "Эксперт"
                                 }[x])
        skill_category = st.selectbox("Категория", 
                                    ["technical", "creative", "management", "communication"], 
                                    key="skill_category",
                                    format_func=lambda x: {
                                        "technical": "Технические",
                                        "creative": "Творческие",
                                        "management": "Управленческие", 
                                        "communication": "Коммуникации"
                                    }[x])
        
        if st.button("Добавить навык", key="add_skill"):
            if skill_name.strip():
                if db.save_skill(st.session_state.user_id, skill_name, skill_level, skill_category):
                    st.success(f"Навык '{skill_name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Ошибка при добавлении навыка")
            else:
                st.error("Введите название навыка")
    
    # Display existing skills
    skills = db.list_skills(st.session_state.user_id)
    if skills:
        st.subheader("📝 Ваши навыки")
        
        # Group by category
        skill_categories = {}
        for skill_id, skill_name, skill_level, category in skills:
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append((skill_id, skill_name, skill_level))
        
        for category, category_skills in skill_categories.items():
            category_name = {
                "technical": "🔧 Технические",
                "creative": "🎨 Творческие", 
                "management": "👥 Управленческие",
                "communication": "💬 Коммуникации"
            }.get(category, f"📂 {category}")
            
            st.write(f"**{category_name}:**")
            for skill_id, skill_name, skill_level in category_skills:
                level_emoji = {
                    "beginner": "⭐", 
                    "intermediate": "⭐⭐",
                    "advanced": "⭐⭐⭐", 
                    "expert": "⭐⭐⭐⭐"
                }.get(skill_level, "⭐")
                
                col_skill, col_delete = st.columns([4, 1])
                with col_skill:
                    st.write(f"• {skill_name} {level_emoji}")
                with col_delete:
                    if st.button("🗑️", key=f"del_skill_{skill_id}", help="Удалить навык"):
                        if db.delete_skill(skill_id, st.session_state.user_id):
                            st.success("Навык удален!")
                            st.rerun()
                        else:
                            st.error("Ошибка при удалении")
    else:
        st.info("Навыки не добавлены. Используйте форму выше для добавления.")

with col2:
    st.subheader("🌍 Языки")
    
    # Add new language form
    with st.expander("➕ Добавить язык", expanded=False):
        language_name = st.text_input("Название языка", key="language_name", help="Например: Английский, Немецкий, Испанский")
        language_level = st.selectbox("Уровень владения", 
                                    ["A1", "A2", "B1", "B2", "C1", "C2"], 
                                    key="language_level",
                                    help="Европейская система уровней CEFR")
        
        if st.button("Добавить язык", key="add_language"):
            if language_name.strip():
                if db.save_language(st.session_state.user_id, language_name, language_level):
                    st.success(f"Язык '{language_name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Ошибка при добавлении языка")
            else:
                st.error("Введите название языка")
    
    # Display existing languages
    languages = db.list_languages(st.session_state.user_id)
    if languages:
        st.subheader("📝 Ваши языки")
        for language_id, language_name, proficiency_level in languages:
            col_lang, col_delete = st.columns([4, 1])
            with col_lang:
                st.write(f"• **{language_name}** - {proficiency_level}")
            with col_delete:
                if st.button("🗑️", key=f"del_lang_{language_id}", help="Удалить язык"):
                    if db.delete_language(language_id, st.session_state.user_id):
                        st.success("Язык удален!")
                        st.rerun()
                    else:
                        st.error("Ошибка при удалении")
    else:
        st.info("Языки не добавлены. Используйте форму выше для добавления.")

# Save to session state for resume generation
if skills or languages:
    st.session_state.data.update({
        "skills": skills,
        "languages": languages
    })

# Navigation help
st.divider()
st.info("💡 После добавления навыков и языков перейдите к генерации резюме в боковой панели.")

# Quick stats
if skills or languages:
    st.subheader("📊 Статистика")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Навыков добавлено", len(skills))
    with col_stat2:
        st.metric("Языков добавлено", len(languages))
