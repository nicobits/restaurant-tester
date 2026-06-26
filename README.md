# Restaurant Tester

> WARNING: INTENTIONALLY VULNERABLE SYSTEM.
> This Django app is deliberately vulnerable and is intended only for local security-training analysis and for testing the internal action at `https://github.com/trailofbits/micro`. Do not deploy it, expose it to the internet, or reuse its patterns in production code.

## System Description

Restaurant Tester is a small Django app for browsing NYC restaurants, reserving a table, viewing or canceling reservations, maintaining a diner profile, and importing menu previews for staff review.

## Subsystems

- `restaurant_tester`: Django project settings, URL routing, ASGI/WSGI entrypoints.
- `reservations.models`: restaurants, reservations, and diner profiles.
- `reservations.views`: public browsing, reservation flow, profile update, and staff tools.
- `reservations.repository`: restaurant search data access.
- `reservations.management.commands.seed_demo_data`: local demo data and users.
- `reservations.templates`: simple server-rendered UI.

## Local Setup

```bash
cd ~/code/restaurant-tester
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Demo users:

- Diner: `guest@example.com` / `guestpass123`
- Staff: `host@example.com` / `staffpass123`
