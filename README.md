# Bethlyn — Django E‑Commerce

A full‑stack Django e‑commerce web application with user accounts, vendor management, product catalog, cart, checkout, orders, and reviews.

## Features
- Custom user model with profiles (sign up, login, logout, password reset).
- Vendor onboarding and management (slugged vendor pages, images, descriptions).
- Category & product catalog with variations (e.g., size/color) and galleries.
- Shopping cart (anonymous + authenticated), merge on login.
- Checkout flow with orders, order items, and payments.
- Ratings & reviews per product.
- Responsive Django templates with reusable snippets (nav, footer, alerts).

## Tech Stack
- **Backend:** Python 3.x, Django (see `requirements.txt`)
- **Database:** SQLite (dev). PostgreSQL recommended for production
- **Templates/Static:** Django Templates, CSS/JS, snippets under `templates/snippets/`
- **Images/Media:** `Pillow`, local `media/` in dev; pluggable storage (`cdn/` module) for prod
- **Auth:** Custom `accounts.AppUser` + `UserProfile`

## Project Structure
```
bethlyn/
├─ manage.py
├─ requirements.txt
├─ db.sqlite3                # dev DB (optional; can delete and re-migrate)
├─ accounts/                 # custom user, auth, profiles
├─ vendors/                  # vendor model & views
├─ category/                 # product categories
├─ store/                    # products, variations, gallery, reviews
├─ carts/                    # cart and cart items
├─ orders/                   # orders, order items, payments
├─ templates/                # pages + snippets (nav, footer, alerts, ...)
├─ static/                   # optional static assets (if present)
├─ media/                    # uploaded images (dev)
└─ bethlyn/                  # project settings, urls, wsgi/asgi
```

## Quick Start (Windows / macOS / Linux)
> **Prerequisite:** Python 3.10+ recommended. Ensure `pip` is available. On Windows, run commands in **Command Prompt** or **PowerShell**; on macOS/Linux, use **Terminal**.

1. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables (optional but recommended)**
   Create a `.env` file in the project root and set:
   ```ini
   DJANGO_SECRET_KEY=change-me
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   # DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit: http://127.0.0.1:8000/

7. **Admin site**
   - `http://127.0.0.1:8000/admin/`

## Static & Media
- Dev uploads live in `media/` (already populated with sample images).
- For production, use a cloud bucket (e.g., S3) via a Django storage backend; the `cdn/` module is set up for pluggable storage.

## Tests
```bash
python manage.py test
```
Add unit tests to each app’s `tests.py` (auth, add-to-cart, checkout, reviews).

## Deployment (Overview)
- Switch DB to PostgreSQL, configure `ALLOWED_HOSTS`, `DEBUG=False`.
- `collectstatic` and serve via CDN or web server.
- Run with Gunicorn/Uvicorn behind Nginx or on a PaaS (Railway/Render/Heroku/PythonAnywhere).
- Secure cookies and HTTPS in production.

### Example Procfile
```
web: gunicorn bethlyn.wsgi
```

## Troubleshooting
- **`django-admin` not recognized** → activate `venv` or use `python manage.py ...`.
- **Missing static/media** → ensure directories & settings are correct.
- **Migrations issues** → `makemigrations` then `migrate`.
- **Admin login fails** → confirm superuser and `AUTH_USER_MODEL` usage.

## License
Student/internal project.

---

*Generated README based on the uploaded codebase.*
