# AI-Dev-Tools Zoomcamp — TODO App (folder: 01-todo)

This folder contains a small Django TODO application used for the "Introduction to AI-Assisted Development" course. It is a pedagogical example showing how to build a simple CRUD web app with Django and how to use development tools (virtualenv or a dependency manager, testing, migrations).

## Key contents
- `manage.py`: Django CLI for running migrations, tests, and the development server.
- `mysite/`: Django project (contains `settings.py`, `urls.py`, `wsgi.py`).
- `core/`: Django app that implements the `Todo` model, views, forms, templates and tests.
- `db.sqlite3`: local SQLite database (generated locally).
- `.venv/`: local Python virtual environment (contains Python interpreter and installed packages).
- `requirements.txt` and `pyproject.toml`: dependency manifests (two possible workflows are shown).

## Implemented features
- Create, edit and delete TODO items (CRUD).
- Assign a due date (`due_date`).
- Mark a TODO as completed (`completed`).
- Django admin configured for the `Todo` model.
- Basic unit tests covering the model and views.

## Prerequisites
- Windows PowerShell (commands below are PowerShell examples).
- Python 3.11+ installed on your machine.

If PowerShell blocks activation scripts, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step-by-step (local development)

1) Open PowerShell and change to the project folder:

```powershell
cd C:\Users\Yann\Desktop\AI-Dev-Tools-Zoomcamp
```

2) (If the virtual environment is not present) Create the virtual environment:

```powershell
python -m venv .venv
```

3) Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
# If activation is blocked, run once with a bypass:
# powershell -ExecutionPolicy Bypass -NoProfile -Command "& '.\.venv\Scripts\Activate.ps1'"
```

4) Install dependencies:

Option A — pip + `requirements.txt` (simple, compatible):

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Option B — using `uv` (modern dependency manager) and `pyproject.toml`:

```powershell
python -m pip install --upgrade pip
pip install uv
uv install        # or `uv add Django` to add Django to the project
uv lock           # create a lockfile for reproducible installs
```

5) Run database migrations:

```powershell
python manage.py migrate
```

6) (Optional) Create a superuser to access the Django admin:

```powershell
python manage.py createsuperuser
```

7) Start the development server:

```powershell
python manage.py runserver
# Open http://127.0.0.1:8000/ in your browser
```

8) Useful routes:
- Home: `/` — links to the TODO list
- TODO app: `/core/` — list and CRUD actions
- Admin: `/admin/` — Django admin interface

## Running tests

Run the project's tests (core app tests included):

```powershell
python manage.py test core -v2
```

The tests cover the `Todo` model and main views (list, create, edit, delete, toggle completion).

## Quick file map (where to look)

- `core/models.py`: `Todo` model.
- `core/forms.py`: `TodoForm` (ModelForm) used for create/edit.
- `core/views.py`: class-based CRUD views and a `toggle_completed` endpoint.
- `core/urls.py`: app routes (`list`, `create`, `edit`, `delete`, `toggle`).
- `core/templates/core/`: templates for list, form and delete confirmation.
- `core/tests.py`: unit tests.

## Teaching notes & suggestions

- This repository is intended as a learning example: install, implement features, run migrations, write tests, run the app.
- You can extend `core/models.py` (e.g. add priority, tags) and then add migrations.
- For production: use a proper WSGI/ASGI server, manage `SECRET_KEY` with environment variables, and move to a production-grade database.

## Possible next improvements

- Add pagination, filtering and sorting for TODO list.
- Add more unit tests for validation and edge cases.
- Add CI (GitHub Actions) to run tests on push.

---
If you want, I can also:
- add a `Makefile` or PowerShell scripts to automate `venv`, `install`, `migrate`, `run` and `test` commands;
- create a short GIF showing the create-a-TODO flow.

Tell me which option you prefer and I will implement it.
