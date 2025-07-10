import streamlit as st
import db

st.set_page_config(page_title="Personal Info - Resume Builder", page_icon="👤", layout="wide")

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("👤 Personal Information")
st.markdown("Please provide your personal details for your resume.")

# Load existing data
saved = db.load_personal_info(st.session_state.user_id)
default_name = saved[0] if saved else ""
default_email = saved[1] if saved else ""
default_phone = saved[2] if saved else ""
saved_photo = saved[3] if saved else None

# Create form
with st.form("personal_info_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        name = st.text_input("Full Name", value=default_name, placeholder="John Doe")
        email = st.text_input("Email", value=default_email, placeholder="john.doe@example.com")
        phone = st.text_input("Phone", value=default_phone, placeholder="+1 (555) 123-4567")
    
    with col2:
        st.markdown("### Profile Photo")
        photo = st.file_uploader("Upload Photo (JPG/PNG)", type=["jpg", "jpeg", "png"], help="Max size: 10MB")
        
        if saved_photo and not photo:
            st.image(saved_photo, caption="Current photo", width=150)
    
    submitted = st.form_submit_button("Save Information", type="primary", use_container_width=True)
    
    if submitted:
        # Validate inputs
        if not name:
            st.error("Please enter your name.")
        elif not email:
            st.error("Please enter your email.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            try:
                # Read photo if uploaded
                photo_bytes = photo.read() if photo else saved_photo
                
                # Validate photo size if new photo
                if photo and photo_bytes and len(photo_bytes) > 10 * 1024 * 1024:
                    st.error("Photo size must be less than 10MB.")
                else:
                    # Save to database
                    db.save_personal_info(st.session_state.user_id, name, email, phone, photo_bytes)
                    
                    # Update session state
                    st.session_state.data.update({
                        "name": name, 
                        "email": email, 
                        "phone": phone,
                        "has_photo": photo_bytes is not None
                    })
                    
                    st.success("✅ Personal information saved successfully!")
                    st.info("You can now proceed to the Education section from the sidebar.")
            except Exception as e:
                st.error(f"Error saving information: {str(e)}")

# Progress indicator
st.markdown("---")
st.progress(0.2, text="Step 1 of 5: Personal Information")
