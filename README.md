# okapy

The Python equivalent of `create-vite` — scaffolds production-ready Python backend projects with an interactive wizard. No more copy-pasting the same Django/FastAPI boilerplate.

## 1. Install

```bash
pip install okapy
```

No install needed:
```bash
uvx okapy create
```

## 2. Create a project

```bash
okapy create
```

Follow the prompts to pick your framework, database, auth, and features.

Skip the prompts for scripting:
```bash
okapy create --name myapi --framework django --type api --defaults
```

## 3. Run it

```bash
cd myapi
source .venv/bin/activate
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

---

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [PRD](docs/PRD.md)
- [Contributing](CONTRIBUTING.md)

MIT
