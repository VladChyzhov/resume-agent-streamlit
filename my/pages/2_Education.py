import streamlit as st
import db

st.set_page_config(page_title="Education - Resume Builder", page_icon="🎓", layout="wide")

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🎓 Education, Diplomas & Certificates")
st.markdown("Upload your educational documents, diplomas, and certificates.")

# File upload section
st.subheader("Upload New Document")
with st.form("education_upload_form"):
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
            db.save_document(doc, st.session_state.user_id, 'education')
            st.success(f"✅ Document '{doc.name}' saved successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Error saving document: {str(e)}")

# Display existing documents
st.markdown("---")
st.subheader("Uploaded Education Documents")

docs = db.list_documents(st.session_state.user_id, 'education')
if docs:
    for doc_id, filename in docs:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"📄 {filename}")
        
        with col2:
            if st.button("Delete", key=f"del_edu_{doc_id}", type="secondary"):
                if db.delete_document(doc_id, st.session_state.user_id):
                    st.success(f"Document '{filename}' deleted.")
                    st.rerun()
else:
    st.info("No education documents uploaded yet. Upload your diplomas, degrees, and certificates above.")

# Progress indicator
st.markdown("---")
st.progress(0.4, text="Step 2 of 5: Education")
