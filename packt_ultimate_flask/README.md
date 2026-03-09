# Packt Ultimate Flask

A multi-module Flask learning workspace containing chapter-based applications from beginner to advanced topics.

## Included Topics
- Flask fundamentals (`00_starter`, `00_flaskr-tutorial`)
- Forms, templates, and ORM
- Authentication and user systems
- Migrations, uploads, i18n, and admin
- REST APIs, sockets, and full app builds (store/forum/twitter clone)

## Folder Naming
Many folders are chapter snapshots, with:
- `- O` meaning completed/reference implementation
- `- X` meaning alternative/in-progress/experimental snapshot

## How to Explore
Open any chapter directory and run the app locally with its own dependencies:
```bash
cd "packt_ultimate_flask/<chapter-folder>"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
