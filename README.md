# Resume Builder - Streamlit Application

A modern, user-friendly resume builder application built with Streamlit. This application allows users to create comprehensive resumes by collecting personal information, education details, work experience, skills, and languages.

## Features

- **User Authentication**: Secure registration and login system with salted password hashing
- **Multi-page Layout**: Organized workflow with progress tracking
- **Personal Information**: Store name, email, phone, and profile photo
- **Document Upload**: Upload education certificates and work experience documents
- **Skills & Languages**: Add technical skills and language proficiencies
- **Data Export**: Export resume data in JSON or text format
- **Responsive UI**: Modern, clean interface with sidebar navigation
- **Data Persistence**: SQLite databases for storing user data and documents

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-builder
```

2. Install the required dependencies:
```bash
pip install -r my/requirements.txt
```

3. Run the application:
```bash
streamlit run my/app.py
```

## Project Structure

```
resume-builder/
├── my/
│   ├── app.py              # Main application entry point
│   ├── db.py               # Database models and functions
│   ├── requirements.txt    # Python dependencies
│   └── pages/              # Streamlit pages
│       ├── 0_Auth.py       # Login and registration
│       ├── 1_Personal_Info.py   # Personal information form
│       ├── 2_Education.py       # Education documents upload
│       ├── 3_Work_Experience.py # Work experience upload
│       ├── 4_Skills_Languages.py # Skills and languages input
│       └── 5_Generate_Resume.py  # Resume preview and export
└── README.md
```

## Database Schema

The application uses two SQLite databases:

### resume.db
Stores uploaded documents:
- `documents` table: Stores file uploads with user association and document type

### user_data.db
Stores user accounts and personal information:
- `users` table: User authentication with secure password hashing
- `personal_info` table: Personal details and profile photos
- `skills_languages` table: Skills and language proficiencies

## Security Features

- **Password Security**: Uses PBKDF2 with SHA256 and salt for password hashing
- **Session Management**: Secure session state management
- **File Size Validation**: 10MB limit on file uploads
- **User Isolation**: Users can only access their own data

## Usage Guide

1. **Registration/Login**: Create a new account or login with existing credentials
2. **Personal Information**: Fill in your basic details and upload a profile photo
3. **Education**: Upload your diplomas, degrees, and certificates
4. **Work Experience**: Upload employment letters and work-related documents
5. **Skills & Languages**: Add your technical skills and language proficiencies
6. **Generate Resume**: Review all information and export your data

## Features Implemented

- ✅ User authentication with secure password storage
- ✅ Multi-page navigation with progress tracking
- ✅ File upload with type validation
- ✅ Document management (upload/delete)
- ✅ Skills and languages management
- ✅ Data export (JSON/Text)
- ✅ Responsive UI with Streamlit components
- ✅ Session state management
- ✅ Error handling and validation

## Planned Features

- 📄 PDF resume generation with professional templates
- 🎨 Multiple resume templates to choose from
- 📧 Email resume functionality
- 🌐 Multi-language support for the interface
- 📊 Resume analytics and tips
- 🔄 Import data from LinkedIn/other sources

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Authentication**: Custom implementation with secure hashing

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
