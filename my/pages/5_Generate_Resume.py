import streamlit as st
import db
from datetime import datetime
import json

st.set_page_config(page_title="Generate Resume - Resume Builder", page_icon="📄", layout="wide")

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("📄 Generate Resume")
st.markdown("Review your information and generate your resume.")

# Get all user data
resume_data = db.get_user_resume_data(st.session_state.user_id)

# Display resume preview
st.subheader("Resume Preview")

# Personal Information Section
with st.expander("👤 Personal Information", expanded=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Name:** {resume_data['personal']['name'] or 'Not provided'}")
        st.markdown(f"**Email:** {resume_data['personal']['email'] or 'Not provided'}")
        st.markdown(f"**Phone:** {resume_data['personal']['phone'] or 'Not provided'}")
    
    with col2:
        if resume_data['personal']['has_photo']:
            st.success("✓ Photo uploaded")
        else:
            st.info("No photo")

# Education Section
with st.expander("🎓 Education", expanded=True):
    if resume_data['education_documents']:
        st.markdown(f"**{len(resume_data['education_documents'])} document(s) uploaded:**")
        for doc_id, filename in resume_data['education_documents']:
            st.markdown(f"- {filename}")
    else:
        st.info("No education documents uploaded")

# Work Experience Section
with st.expander("💼 Work Experience", expanded=True):
    if resume_data['work_documents']:
        st.markdown(f"**{len(resume_data['work_documents'])} document(s) uploaded:**")
        for doc_id, filename in resume_data['work_documents']:
            st.markdown(f"- {filename}")
    else:
        st.info("No work experience documents uploaded")

# Skills Section
with st.expander("🛠️ Skills", expanded=True):
    if resume_data['skills']:
        skills_list = resume_data['skills'].strip().split('\n')
        skills_list = [s.strip() for s in skills_list if s.strip()]
        if skills_list:
            st.markdown("**Technical Skills:**")
            # Display skills in columns
            cols = st.columns(3)
            for i, skill in enumerate(skills_list):
                cols[i % 3].markdown(f"• {skill}")
        else:
            st.info("No skills added")
    else:
        st.info("No skills added")

# Languages Section
with st.expander("🌍 Languages", expanded=True):
    if resume_data['languages']:
        languages_list = resume_data['languages'].strip().split('\n')
        languages_list = [l.strip() for l in languages_list if l.strip()]
        if languages_list:
            st.markdown("**Language Proficiencies:**")
            for lang in languages_list:
                st.markdown(f"• {lang}")
        else:
            st.info("No languages added")
    else:
        st.info("No languages added")

# Export Options
st.markdown("---")
st.subheader("Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Generate PDF Resume", type="primary", use_container_width=True):
        st.warning("PDF generation is not yet implemented. This feature will be added soon.")
        st.info("In a production environment, this would use a library like ReportLab or WeasyPrint to generate a professional PDF resume.")

with col2:
    # Export as JSON
    if st.button("💾 Export as JSON", use_container_width=True):
        json_data = json.dumps(resume_data, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col3:
    # Export as text
    if st.button("📝 Export as Text", use_container_width=True):
        text_content = f"""RESUME
        
Name: {resume_data['personal']['name']}
Email: {resume_data['personal']['email']}
Phone: {resume_data['personal']['phone']}

EDUCATION:
{chr(10).join([f"- {doc[1]}" for doc in resume_data['education_documents']])}

WORK EXPERIENCE:
{chr(10).join([f"- {doc[1]}" for doc in resume_data['work_documents']])}

SKILLS:
{resume_data['skills']}

LANGUAGES:
{resume_data['languages']}
"""
        st.download_button(
            label="Download Text",
            data=text_content,
            file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# Completion message
st.markdown("---")
st.progress(1.0, text="Step 5 of 5: Generate Resume - Complete!")

# Tips
with st.info("💡 **Tips for a better resume:**"):
    st.markdown("""
    - Ensure all your information is up to date
    - Upload clear, high-quality documents
    - List skills relevant to your target position
    - Include language proficiencies if applying internationally
    - Keep your resume concise and well-organized
    """)

# Add a note about PDF generation
st.markdown("---")
st.markdown("### 🚧 Note about PDF Generation")
st.markdown("""
The PDF generation feature is currently under development. In a production environment, this would:
- Generate a professionally formatted PDF resume
- Include your photo (if uploaded)
- Organize all information in a clean, readable layout
- Allow customization of resume templates
- Support multiple export formats

For now, you can export your data as JSON or text format.
""")
