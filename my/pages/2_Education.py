import streamlit as st
import db

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🎓 Образование, дипломы, сертификаты")

# File upload section
st.subheader("📄 Загрузка документов")

with st.expander("➕ Добавить документ об образовании", expanded=True):
    doc = st.file_uploader(
        "Выберите файл", 
        key="edu_upload",
        type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
        help="Поддерживаемые форматы: PDF, JPG, PNG, DOC, DOCX"
    )
    
    # Document type selection
    doc_type = st.selectbox(
        "Тип документа",
        ["diploma", "certificate", "transcript", "other"],
        format_func=lambda x: {
            "diploma": "🎓 Диплом",
            "certificate": "📜 Сертификат", 
            "transcript": "📋 Справка/Выписка",
            "other": "📄 Другое"
        }[x],
        help="Выберите тип загружаемого документа"
    )
    
    if st.button("Сохранить документ", key="edu_save", type="primary"):
        if doc:
            # File size validation (max 10MB)
            if doc.size > 10 * 1024 * 1024:
                st.error("Файл слишком большой. Максимальный размер: 10MB")
            else:
                if db.save_document(doc, st.session_state.user_id, f"education_{doc_type}"):
                    st.success(f"Документ '{doc.name}' успешно сохранен!")
                    st.rerun()
                else:
                    st.error("Ошибка при сохранении документа")
        else:
            st.error("Выберите файл для загрузки")

# Display existing documents
st.subheader("📚 Загруженные документы")

# Get all education-related documents
education_docs = []
for category in ["education_diploma", "education_certificate", "education_transcript", "education_other"]:
    docs = db.list_documents(st.session_state.user_id, category)
    education_docs.extend(docs)

if education_docs:
    # Group documents by type
    doc_groups = {
        "education_diploma": [],
        "education_certificate": [], 
        "education_transcript": [],
        "education_other": []
    }
    
    for doc_id, filename, category in education_docs:
        if category in doc_groups:
            doc_groups[category].append((doc_id, filename))
    
    # Display grouped documents
    for category, docs in doc_groups.items():
        if docs:
            category_name = {
                "education_diploma": "🎓 Дипломы",
                "education_certificate": "📜 Сертификаты",
                "education_transcript": "📋 Справки/Выписки", 
                "education_other": "📄 Другие документы"
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
        "education_documents": len(education_docs),
        "education_doc_details": education_docs
    })
else:
    st.info("📝 Документы об образовании не загружены. Используйте форму выше для добавления документов.")

# Additional education information form
st.subheader("📝 Дополнительная информация об образовании")

with st.expander("✏️ Добавить информацию", expanded=False):
    institution = st.text_input("Учебное заведение", help="Название университета, колледжа или школы")
    degree = st.text_input("Степень/Квалификация", help="Например: Бакалавр, Магистр, Специалист")
    field = st.text_input("Специальность", help="Область изучения или специальность")
    
    col_start, col_end = st.columns(2)
    with col_start:
        start_year = st.number_input("Год поступления", min_value=1950, max_value=2030, value=2020)
    with col_end:
        end_year = st.number_input("Год окончания", min_value=1950, max_value=2030, value=2024)
    
    gpa = st.text_input("Средний балл (если есть)", help="Например: 4.5/5.0 или отлично")
    honors = st.text_input("Награды/Отличия", help="Например: красный диплом, стипендия")
    
    if st.button("Сохранить информацию об образовании"):
        education_info = {
            "institution": institution,
            "degree": degree, 
            "field": field,
            "start_year": start_year,
            "end_year": end_year,
            "gpa": gpa,
            "honors": honors
        }
        
        # Save to session state (in a real app, this would go to database)
        if "education_info" not in st.session_state.data:
            st.session_state.data["education_info"] = []
        st.session_state.data["education_info"].append(education_info)
        
        st.success("Информация об образовании сохранена!")

# Navigation help
st.divider()
st.info("💡 После загрузки документов перейдите к разделу 'Опыт работы' в боковой панели.")

# Quick stats
if education_docs:
    st.subheader("📊 Статистика")
    st.metric("Документов загружено", len(education_docs))
