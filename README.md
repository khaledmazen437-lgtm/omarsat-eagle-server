OMARSAT — Eagle Server Store (Django)

> موقع OMARSAT / Eagle Server — عرض باقات سيرفرات IPTV و CCcam، أخبار السيرفر، وتقارير الحالة. مبني بـ Django.

A Django website for the OMARSAT server store: IPTV and CCcam plan listings, server status reports and news, with an admin area for managing plans and reports.

## Features

- `ServerPlan` model split by type (`iptv` / `cccam`) with images
- `ServerReport` status reports and `ServerNews` news feed
- Django admin for content management
- Static front-end (custom CSS/JS in `static/`)

## Tech Stack

- Python 3.13 + Django
- SQLite by default (see `core/settings.py`)
- `build.sh` for deployment builds

## Running locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Notes / hardening checklist

- `DEBUG = True` and `ALLOWED_HOSTS = ['*']` are set — set DEBUG=False and restrict hosts in production.
- Remove `ngrok.exe` (~31 MB) and `__pycache__/` from the repo and add them to `.gitignore`; use Git LFS or releases for binaries.
- Move `SECRET_KEY` and any credentials to environment variables.

