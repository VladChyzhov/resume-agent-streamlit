import streamlit as st
import db

st.set_page_config(page_title="Work Experience - Resume Builder", page_icon="💼", layout="wide")

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("💼 Work Experience")
st.markdown("Upload documents related to your work experience, such as employment letters, recommendations, or project descriptions.")

# File upload section
st.subheader("Upload New Document")
with st.form("work_upload_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        doc = st.file_uploader(
            "Choose a document", 
            type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            help="Supported formats: PDF, JPG, PNG, DOC, DOCX (Max 10MB)"
        )
    
    with col2:
        st.markdown("&nbsp;")  # Spacing
        submitted = st.form_submit_button("Save Document", type="primary", use_container_width=True)
    
    if submitted and doc:
        try:
            db.save_document(doc, st.session_state.user_id, 'work')
            st.success(f"✅ Document '{doc.name}' saved successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Error saving document: {str(e)}")

# Display existing documents
st.markdown("---")
st.subheader("Uploaded Work Experience Documents")

docs = db.list_documents(st.session_state.user_id, 'work')
if docs:
    for doc_id, filename in docs:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"📄 {filename}")
        
        with col2:
            if st.button("Delete", key=f"del_work_{doc_id}", type="secondary"):
                if db.delete_document(doc_id, st.session_state.user_id):
                    st.success(f"Document '{filename}' deleted.")
                    st.rerun()
else:
    st.info("No work experience documents uploaded yet. Upload your employment letters, recommendations, or certificates above.")

# Progress indicator
st.markdown("---")
st.progress(0.6, text="Step 3 of 5: Work Experience")
