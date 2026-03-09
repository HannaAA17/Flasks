# Coursera Flask Tasks App

A simple task management web app built with Flask as part of coursework exercises.

## Features
- Create and manage tasks
- Form handling with Flask-WTF
- Server-rendered templates
- SQLite-backed persistence (via the app configuration)

## Project Structure
- `app.py` — application entry point
- `routes.py` — route handlers
- `models.py` — data models
- `forms.py` — form definitions
- `templates/` — HTML templates

## Getting Started
```bash
cd coursera_flask-tasks-app
python -m venv .venv
source .venv/bin/activate
pip install flask flask-wtf
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.
