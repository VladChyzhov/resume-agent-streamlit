import streamlit as st
import db
from datetime import datetime
import json

def generate_text_resume(personal_info, user_data, skills, languages, education_docs, work_docs):
    """Generate a text version of the resume"""
    lines = []
    
    # Header
    if personal_info:
        lines.append("=" * 50)
        lines.append(f"РЕЗЮМЕ: {personal_info[0] or 'Имя не указано'}")
        lines.append("=" * 50)
        lines.append("")
        
        if personal_info[1]:
            lines.append(f"Email: {personal_info[1]}")
        if personal_info[2]:
            lines.append(f"Телефон: {personal_info[2]}")
        lines.append("")
    
    # Work Experience
    if "work_experience" in user_data and user_data["work_experience"]:
        lines.append("ОПЫТ РАБОТЫ")
        lines.append("-" * 20)
        for work in user_data["work_experience"]:
            lines.append(f"{work['position']} - {work['company']}")
            start_date = work['start_date'] if work['start_date'] else "Не указано"
            end_date = "по настоящее время" if work['is_current'] else (work['end_date'] if work['end_date'] else "Не указано")
            lines.append(f"Период: {start_date} - {end_date}")
            
            if work['responsibilities']:
                lines.append("Обязанности:")
                for resp in work['responsibilities'].split('\n'):
                    if resp.strip():
                        lines.append(f"• {resp.strip()}")
            lines.append("")
    
    # Education
    if "education_info" in user_data and user_data["education_info"]:
        lines.append("ОБРАЗОВАНИЕ")
        lines.append("-" * 20)
        for edu in user_data["education_info"]:
            lines.append(f"{edu['degree']} - {edu['field']}")
            lines.append(f"{edu['institution']}")
            lines.append(f"{edu['start_year']} - {edu['end_year']}")
            if edu['gpa']:
                lines.append(f"Средний балл: {edu['gpa']}")
            lines.append("")
    
    # Skills
    if skills:
        lines.append("НАВЫКИ")
        lines.append("-" * 20)
        for skill_id, skill_name, skill_level, category in skills:
            lines.append(f"• {skill_name} ({skill_level})")
        lines.append("")
    
    # Languages
    if languages:
        lines.append("ЯЗЫКИ")
        lines.append("-" * 20)
        for lang_id, language_name, proficiency_level in languages:
            lines.append(f"• {language_name} - {proficiency_level}")
    
    return "\n".join(lines)

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("📄 Генерация резюме")

# Get user data
user_data = st.session_state.get("data", {})
user_id = st.session_state.user_id

# Load fresh data from database
personal_info = db.load_personal_info(user_id)
skills = db.list_skills(user_id)
languages = db.list_languages(user_id)

# Get document counts
education_docs = []
work_docs = []
for category in ["education_diploma", "education_certificate", "education_transcript", "education_other"]:
    education_docs.extend(db.list_documents(user_id, category))

for category in ["work_employment_certificate", "work_recommendation", "work_contract", "work_portfolio", "work_other"]:
    work_docs.extend(db.list_documents(user_id, category))

# Resume generation options
st.subheader("⚙️ Параметры резюме")

col1, col2 = st.columns(2)
with col1:
    resume_style = st.selectbox(
        "Стиль резюме",
        ["professional", "modern", "creative"],
        format_func=lambda x: {
            "professional": "🏢 Профессиональный",
            "modern": "💼 Современный", 
            "creative": "🎨 Креативный"
        }[x]
    )

with col2:
    include_photo = st.checkbox("Включить фото", value=True if personal_info and personal_info[3] else False)

# Resume preview
st.subheader("👀 Предварительный просмотр резюме")

if personal_info:
    # Header section
    st.markdown("---")
    
    # Create header with photo if available
    if include_photo and personal_info[3]:
        col_photo, col_info = st.columns([1, 3])
        with col_photo:
            st.image(personal_info[3], width=150, caption="")
        with col_info:
            st.markdown(f"# {personal_info[0] or 'Имя не указано'}")
            if personal_info[1]:
                st.markdown(f"📧 **Email:** {personal_info[1]}")
            if personal_info[2]:
                st.markdown(f"📱 **Телефон:** {personal_info[2]}")
    else:
        st.markdown(f"# {personal_info[0] or 'Имя не указано'}")
        if personal_info[1]:
            st.markdown(f"📧 **Email:** {personal_info[1]}")
        if personal_info[2]:
            st.markdown(f"📱 **Телефон:** {personal_info[2]}")
    
    st.markdown("---")
    
    # Work Experience Section
    if "work_experience" in user_data and user_data["work_experience"]:
        st.markdown("## 💼 Опыт работы")
        for work in user_data["work_experience"]:
            st.markdown(f"### {work['position']}")
            st.markdown(f"**{work['company']}**")
            
            # Format dates
            start_date = work['start_date'] if work['start_date'] else "Не указано"
            if work['is_current']:
                end_date = "по настоящее время"
            else:
                end_date = work['end_date'] if work['end_date'] else "Не указано"
            
            st.markdown(f"*{start_date} - {end_date}*")
            
            if work['company_description']:
                st.markdown(f"**О компании:** {work['company_description']}")
            
            if work['responsibilities']:
                st.markdown("**Обязанности и достижения:**")
                # Split by lines and format as bullet points
                responsibilities = work['responsibilities'].split('\n')
                for resp in responsibilities:
                    if resp.strip():
                        st.markdown(f"• {resp.strip()}")
            
            if work['technologies']:
                st.markdown(f"**Технологии:** {work['technologies']}")
            
            st.markdown("")
    
    # Education Section
    if "education_info" in user_data and user_data["education_info"]:
        st.markdown("## 🎓 Образование")
        for edu in user_data["education_info"]:
            st.markdown(f"### {edu['degree']} - {edu['field']}")
            st.markdown(f"**{edu['institution']}**")
            st.markdown(f"*{edu['start_year']} - {edu['end_year']}*")
            
            if edu['gpa']:
                st.markdown(f"**Средний балл:** {edu['gpa']}")
            if edu['honors']:
                st.markdown(f"**Награды и отличия:** {edu['honors']}")
            st.markdown("")
    
    # Skills Section
    if skills:
        st.markdown("## 🛠️ Навыки")
        
        # Group skills by category
        skill_categories = {}
        for skill_id, skill_name, skill_level, category in skills:
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append((skill_name, skill_level))
        
        for category, category_skills in skill_categories.items():
            category_name = {
                "technical": "💻 Технические навыки",
                "creative": "🎨 Творческие навыки",
                "management": "👥 Управленческие навыки",
                "communication": "💬 Коммуникационные навыки"
            }.get(category, f"📂 {category}")
            
            st.markdown(f"### {category_name}")
            
            # Display skills in columns for better layout
            skill_cols = st.columns(3)
            for i, (skill_name, skill_level) in enumerate(category_skills):
                level_display = {
                    "beginner": "⭐ Начинающий",
                    "intermediate": "⭐⭐ Средний",
                    "advanced": "⭐⭐⭐ Продвинутый",
                    "expert": "⭐⭐⭐⭐ Эксперт"
                }.get(skill_level, skill_level)
                
                with skill_cols[i % 3]:
                    st.markdown(f"**{skill_name}**")
                    st.caption(level_display)
            st.markdown("")
    
    # Languages Section
    if languages:
        st.markdown("## 🌍 Языки")
        lang_cols = st.columns(2)
        for i, (lang_id, language_name, proficiency_level) in enumerate(languages):
            with lang_cols[i % 2]:
                st.markdown(f"**{language_name}** - {proficiency_level}")
    
    # Documents Section
    if education_docs or work_docs:
        st.markdown("## 📁 Приложенные документы")
        
        col_edu, col_work = st.columns(2)
        
        with col_edu:
            if education_docs:
                st.markdown("### 🎓 Образование")
                st.markdown(f"Документов: {len(education_docs)}")
        
        with col_work:
            if work_docs:
                st.markdown("### 💼 Опыт работы")
                st.markdown(f"Документов: {len(work_docs)}")
    
    st.markdown("---")
    
    # Export options
    st.subheader("📤 Экспорт резюме")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        if st.button("📄 Экспорт в текст", type="secondary"):
            # Generate text version
            resume_text = generate_text_resume(personal_info, user_data, skills, languages, education_docs, work_docs)
            st.download_button(
                label="⬇️ Скачать TXT",
                data=resume_text,
                file_name=f"resume_{personal_info[0] or 'user'}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col_export2:
        if st.button("📋 Копировать в буфер", type="secondary"):
            resume_text = generate_text_resume(personal_info, user_data, skills, languages, education_docs, work_docs)
            st.code(resume_text, language="text")
            st.success("Резюме готово для копирования!")
    
    with col_export3:
        st.button("📄 Экспорт в PDF", type="primary", help="Функция в разработке")
        st.caption("PDF экспорт будет доступен в следующей версии")

else:
    st.warning("⚠️ Сначала заполните персональные данные на соответствующей странице.")
    if st.button("Перейти к персональным данным"):
        st.switch_page("pages/1_Personal_Info.py")

# Statistics
st.subheader("📊 Статистика заполнения")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    personal_complete = 1 if personal_info and personal_info[0] else 0
    st.metric("Персональные данные", "✅" if personal_complete else "❌")

with col_stat2:
    work_complete = len(user_data.get("work_experience", []))
    st.metric("Опыт работы", f"{work_complete} записей")

with col_stat3:
    skills_complete = len(skills)
    st.metric("Навыки", f"{skills_complete} шт.")

with col_stat4:
    docs_complete = len(education_docs) + len(work_docs)
    st.metric("Документы", f"{docs_complete} шт.")

# Completion progress
total_sections = 4
completed_sections = 0
if personal_complete:
    completed_sections += 1
if work_complete > 0:
    completed_sections += 1
if skills_complete > 0:
    completed_sections += 1
if docs_complete > 0:
    completed_sections += 1

progress = completed_sections / total_sections
st.progress(progress)
st.caption(f"Заполнено: {completed_sections}/{total_sections} разделов ({progress:.0%})")
