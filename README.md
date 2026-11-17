# Vande Bharat Developers

A responsive Django real-estate website with public project discovery, project and contact enquiries, image galleries, and a protected Django administration dashboard.

## Run locally

1. Use Python 3.10 or later.
2. Copy `.env.example` to `.env` for local development and update its settings.
3. Install dependencies: `python -m pip install -r requirements.txt`.
4. Apply database migrations: `python manage.py migrate`.
5. Create an administrator login: `python manage.py createsuperuser`.
6. Start the development server: `python manage.py runserver`.
7. Visit `http://127.0.0.1:8000/`. Manage projects, gallery images, and enquiries at `/admin/`.

The site starts with SQLite and includes a "South Future City" draft whose location and listing details should be updated in the admin before publishing. The `.env` file is loaded for local development; set deployment environment variables directly in production. Set `DATABASE_URL` to a PostgreSQL connection URL in production, and set a unique `SECRET_KEY`, `DEBUG=False`, and your real `ALLOWED_HOSTS`.

## Business details

Set `COMPANY_PHONE`, `COMPANY_EMAIL`, `COMPANY_ADDRESS`, `COMPANY_WHATSAPP_NUMBER` (digits only, with the country code), and `COMPANY_MAP_QUERY` to show the real business contact information, enable the WhatsApp link, and point the embedded map at the correct location. The project template deliberately does not invent a phone number or office address.

Add and update projects and their images in the staff-only Django admin. Project records, submitted enquiries, availability, pricing, gallery images, and customer testimonials are stored in the configured database and media storage. Testimonials stay hidden until a staff member publishes them; only publish comments with the customer's permission. Replace the sample project's placeholder details and add verified company milestones and genuine contact information before launch.

## Production

Configure PostgreSQL with `DATABASE_URL`, use durable media storage for project images, and serve those images through a properly configured media host or CDN. Keep the enquiry database private and the admin restricted. Then run:

```text
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn vande_bharat.wsgi:application
```

Set HTTPS, `CSRF_TRUSTED_ORIGINS` (comma-separated full origins) if needed, a stable secret, and properly restricted hostnames. HTTPS redirection and secure cookies are enabled when `DEBUG=False`; set `SECURE_SSL_REDIRECT=False` only if TLS terminates outside the app and that proxy already enforces HTTPS. Set `TRUST_X_FORWARDED_PROTO=True` only behind a trusted proxy that strips incoming forwarded-protocol headers and sets `X-Forwarded-Proto` itself. Create staff accounts using `createsuperuser`; Django's authentication, permission checks, CSRF protection, password validation, and admin permissions protect the dashboard.

Run the focused checks with `python manage.py test` and the Django deployment checks with `python manage.py check --deploy`.
