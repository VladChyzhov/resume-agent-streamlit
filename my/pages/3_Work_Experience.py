import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("💼 Опыт работы")

# File upload section
st.subheader("📄 Загрузка документов")

with st.expander("➕ Добавить документ о работе", expanded=True):
    doc = st.file_uploader(
        "Выберите файл", 
        key="exp_upload",
        type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
        help="Поддерживаемые форматы: PDF, JPG, PNG, DOC, DOCX"
    )
    
    # Document type selection
    doc_type = st.selectbox(
        "Тип документа",
        ["employment_certificate", "recommendation", "contract", "portfolio", "other"],
        format_func=lambda x: {
            "employment_certificate": "📋 Справка о работе",
            "recommendation": "📝 Рекомендательное письмо", 
            "contract": "📄 Трудовой договор",
            "portfolio": "🎨 Портфолио/Образцы работ",
            "other": "📄 Другое"
        }[x],
        help="Выберите тип загружаемого документа"
    )
    
    if st.button("Сохранить документ", key="exp_save", type="primary"):
        if doc:
            # File size validation (max 10MB)
            if doc.size > 10 * 1024 * 1024:
                st.error("Файл слишком большой. Максимальный размер: 10MB")
            else:
                if db.save_document(doc, st.session_state.user_id, f"work_{doc_type}"):
                    st.success(f"Документ '{doc.name}' успешно сохранен!")
                    st.rerun()
                else:
                    st.error("Ошибка при сохранении документа")
        else:
            st.error("Выберите файл для загрузки")

# Display existing documents
st.subheader("📚 Загруженные документы")

# Get all work-related documents
work_docs = []
for category in ["work_employment_certificate", "work_recommendation", "work_contract", "work_portfolio", "work_other"]:
    docs = db.list_documents(st.session_state.user_id, category)
    work_docs.extend(docs)

if work_docs:
    # Group documents by type
    doc_groups = {
        "work_employment_certificate": [],
        "work_recommendation": [], 
        "work_contract": [],
        "work_portfolio": [],
        "work_other": []
    }
    
    for doc_id, filename, category in work_docs:
        if category in doc_groups:
            doc_groups[category].append((doc_id, filename))
    
    # Display grouped documents
    for category, docs in doc_groups.items():
        if docs:
            category_name = {
                "work_employment_certificate": "📋 Справки о работе",
                "work_recommendation": "📝 Рекомендательные письма",
                "work_contract": "📄 Трудовые договоры", 
                "work_portfolio": "🎨 Портфолио/Образцы работ",
                "work_other": "📄 Другие документы"
            }[category]
            
            st.write(f"**{category_name}:**")
            for doc_id, filename in docs:
                col_doc, col_info = st.columns([3, 1])
                with col_doc:
                    st.write(f"• {filename}")
                with col_info:
                    st.caption(f"ID: {doc_id}")
            st.write("")  # Add spacing
    
    # Save document info to session state
    st.session_state.data.update({
        "work_documents": len(work_docs),
        "work_doc_details": work_docs
    })
else:
    st.info("📝 Документы об опыте работы не загружены. Используйте форму выше для добавления документов.")

# Work experience information form
st.subheader("💼 Информация об опыте работы")

with st.expander("✏️ Добавить информацию о работе", expanded=False):
    company = st.text_input("Название компании", help="Название организации или компании")
    position = st.text_input("Должность", help="Ваша должность в компании")
    
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input("Дата начала работы")
    with col_end:
        is_current = st.checkbox("Работаю в настоящее время")
        if not is_current:
            end_date = st.date_input("Дата окончания работы")
        else:
            end_date = None
    
    responsibilities = st.text_area(
        "Обязанности и достижения", 
        height=100,
        help="Опишите ваши основные обязанности и достижения на этой должности"
    )
    
    technologies = st.text_input(
        "Использованные технологии/инструменты", 
        help="Например: Python, Excel, CRM системы"
    )
    
    company_description = st.text_input(
        "Описание компании (кратко)", 
        help="Сфера деятельности компании"
    )
    
    if st.button("Сохранить информацию о работе"):
        work_info = {
            "company": company,
            "position": position,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "is_current": is_current,
            "responsibilities": responsibilities,
            "technologies": technologies,
            "company_description": company_description
        }
        
        # Save to session state (in a real app, this would go to database)
        if "work_experience" not in st.session_state.data:
            st.session_state.data["work_experience"] = []
        st.session_state.data["work_experience"].append(work_info)
        
        st.success("Информация об опыте работы сохранена!")

# Display saved work experience
if "work_experience" in st.session_state.data and st.session_state.data["work_experience"]:
    st.subheader("📋 Сохраненный опыт работы")
    
    for i, work in enumerate(st.session_state.data["work_experience"]):
        with st.expander(f"{work['position']} в {work['company']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Компания:** {work['company']}")
                st.write(f"**Должность:** {work['position']}")
            with col2:
                start = work['start_date'] if work['start_date'] else "Не указано"
                end = work['end_date'] if work['end_date'] else ("по настоящее время" if work['is_current'] else "Не указано")
                st.write(f"**Период:** {start} - {end}")
                if work['company_description']:
                    st.write(f"**О компании:** {work['company_description']}")
            
            if work['responsibilities']:
                st.write(f"**Обязанности и достижения:**")
                st.write(work['responsibilities'])
            
            if work['technologies']:
                st.write(f"**Технологии:** {work['technologies']}")
            
            if st.button(f"Удалить запись {i+1}", key=f"delete_work_{i}"):
                st.session_state.data["work_experience"].pop(i)
                st.rerun()

# Navigation help
st.divider()
st.info("💡 После добавления информации о работе перейдите к разделу 'Навыки и языки' в боковой панели.")

# Quick stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Документов загружено", len(work_docs))
with col2:
    work_count = len(st.session_state.data.get("work_experience", []))
    st.metric("Мест работы добавлено", work_count)
