# Resume Agent Streamlit

This repository contains a minimal Streamlit application for assembling resume data.

## Running

Install dependencies and start the app. The `my/requirements.txt` file
contains only the small set of packages used by the demo (primarily
`streamlit` and `requests`):

```bash
pip install -r my/requirements.txt
streamlit run my/app.py
```

## Database

The application stores form data in a local SQLite database. The file
`my/resume.db` will be created automatically on first run and reused on
subsequent launches.

Start the app with data persistence enabled using:

```bash
streamlit run my/app.py
```

All information will be read from and written to `my/resume.db`.
