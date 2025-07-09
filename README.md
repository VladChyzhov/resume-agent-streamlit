# Resume Agent Streamlit

This repository contains a minimal Streamlit application for assembling resume data.

## Running

Install dependencies and start the app:

```bash
pip install -r my/requirements.txt
streamlit run my/app.py
```

## Database

All data is stored in a SQLite database. By default the file `resume.db` is placed
in the `my` directory. The database will be created automatically on first run.

To launch the app and keep your data between sessions, execute:

```bash
streamlit run my/app.py
```

The application will read and write data to `my/resume.db`.
