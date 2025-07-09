# Resume Agent Streamlit

This repository contains a minimal Streamlit application for assembling resume data.

## Running

Install the required dependencies and start the Streamlit server. The
`my/requirements.txt` file contains only the small set of packages used by
the demo (primarily `streamlit` and `requests`):

```bash
pip install -r my/requirements.txt
streamlit run my/app.py
```

## Database

Two SQLite databases are created in the `my/` directory when the app first
runs:

* **`my/resume.db`** – stores uploaded documents such as diplomas and work
  experience files.
* **`my/user_data.db`** – stores user accounts and personal information that
  is filled out on the forms.

Both files are reused on subsequent launches.

## Multi-page layout

The interface is organised as a series of numbered pages:

1. **0_Auth** – login and registration.
2. **1_Personal_Info** – collect name, email, phone and an optional photo.
3. **2_Education** – upload diplomas and certificates.
4. **3_Work_Experience** – upload documents describing prior work.
5. **4_Skills_Languages** – placeholder for skills and language inputs.
6. **5_Generate_Resume** – shows the gathered data and will later export a
   PDF.

Start the application from the repository root with:

```bash
streamlit run my/app.py
```
