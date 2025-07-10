import streamlit as st
import db

st.set_page_config(page_title="Skills & Languages - Resume Builder", page_icon="🛠️", layout="wide")

if st.session_state.get("user_id") is None:
    st.switch_page("pages/0_Auth.py")

st.title("🛠️ Skills & 🌍 Languages")
st.markdown("Add your technical skills and language proficiencies.")

# Load existing data
saved_data = db.load_skills_languages(st.session_state.user_id)
default_skills = saved_data[0] if saved_data else ""
default_languages = saved_data[1] if saved_data else ""

# Create two columns for skills and languages
col1, col2 = st.columns(2)

with col1:
    st.subheader("Technical Skills")
    skills = st.text_area(
        "List your skills (one per line)",
        value=default_skills,
        height=200,
        placeholder="Python\nJavaScript\nReact\nSQL\nGit\nDocker\nAWS\nMachine Learning",
        help="Enter each skill on a new line"
    )
    
    # Common skills quick add
    st.markdown("**Quick add common skills:**")
    skill_cols = st.columns(3)
    common_skills = [
        "Python", "JavaScript", "Java", "React", "Node.js", "SQL",
        "Git", "Docker", "AWS", "Machine Learning", "Data Analysis", "Agile"
    ]
    
    for i, skill in enumerate(common_skills):
        col = skill_cols[i % 3]
        with col:
            if st.button(skill, key=f"skill_{skill}", use_container_width=True):
                if skill not in skills:
                    skills = skills.strip()
                    if skills:
                        skills += f"\n{skill}"
                    else:
                        skills = skill
                    st.rerun()

with col2:
    st.subheader("Languages")
    languages = st.text_area(
        "List languages and proficiency",
        value=default_languages,
        height=200,
        placeholder="English - Native\nSpanish - Fluent\nFrench - Intermediate\nMandarin - Basic",
        help="Format: Language - Proficiency level"
    )
    
    # Language proficiency helper
    st.markdown("**Proficiency levels:**")
    st.markdown("""
    - **Native** - Mother tongue
    - **Fluent** - Full professional proficiency
    - **Advanced** - Professional working proficiency
    - **Intermediate** - Limited working proficiency
    - **Basic** - Elementary proficiency
    """)

# Save button
st.markdown("---")
if st.button("Save Skills & Languages", type="primary", use_container_width=True):
    try:
        db.save_skills_languages(st.session_state.user_id, skills, languages)
        
        # Update session state
        st.session_state.data.update({
            "skills": skills,
            "languages": languages
        })
        
        st.success("✅ Skills and languages saved successfully!")
        st.info("You can now proceed to generate your resume from the sidebar.")
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")

# Progress indicator
st.markdown("---")
st.progress(0.8, text="Step 4 of 5: Skills & Languages")
