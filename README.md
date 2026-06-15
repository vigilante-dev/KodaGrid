# CodeSavannah Academy Django Website

A professional, responsive technology education website for a coding academy or youth digital skills organization. The project uses Python, Django, Django templates, HTML5, and custom CSS only.

## Features

- Public pages for Home, About, Courses, Events, Blog, Gallery, and Contact.
- Django authentication for student registration, login, logout, profile, and password reset.
- Django Admin management for students, courses, events, event registrations, blog posts, testimonials, gallery items, newsletter subscribers, and contact messages.
- W3Schools-style learning paths for programming, web, mobile, databases, cloud, cybersecurity, and AI with lessons, exercises, quizzes, notes, and projects.
- Student portal with live progress, upcoming assignments, certificates, recommended paths, and mentorship activity.
- Google Classroom-style workspace with class-code joining, trainer/staff class creation, class streams, materials, attendance marking, assignment submissions, and grade feedback.
- Admin-managed fee plans, trainer applications, mentorship bookings, resources, job opportunities, community challenges, and certificate verification records.
- Search and filtering for courses, events, and blog articles.
- SEO-friendly slug URLs for courses, events, and blog posts.
- Contact form, newsletter signup, CSRF protection, form validation, and console email notifications.
- Media upload support for course images, profile pictures, blog images, gallery images, and testimonials.
- Image analysis command that optimizes images, classifies educational relevance, generates captions, and recommends page placements.
- Pagination for listing pages.
- Optional Google Analytics hook through `DJANGO_ANALYTICS_ID`.
- Admin-manageable featured video story with homepage video playback and a designed motion-poster fallback.
- Responsive custom CSS with smooth hover transitions, accessible forms, dark-mode-aware colors, and no frontend framework.
- Seed migration with demo courses, events, testimonials, blog posts, and gallery entries.

## Project Structure

```text
accounts/   Student profiles and authentication views
blog/       Blog post model, list view, detail view, and admin
config/     Project settings and root URL configuration
contact/    Contact form, message model, and admin
core/       Home, About, testimonials, newsletter, and seeded content
courses/    Course catalog, search, detail pages, and admin
events/     Events, registrations, list/detail views, and admin
gallery/    Gallery model, filters, and admin
static/     Custom CSS and project-native visual assets
templates/  Reusable Django templates
```

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate
```

Analyze and optimize the supplied academy images:

```powershell
python manage.py analyze_academy_images --source images
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Environment Variables

For production, set these values outside the codebase:

```text
DJANGO_SECRET_KEY=replace-with-a-secure-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
DJANGO_DB_ENGINE=postgresql
POSTGRES_DB=codesavannah
POSTGRES_USER=codesavannah
POSTGRES_PASSWORD=replace-with-a-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=CodeSavannah Academy <hello@example.com>
DJANGO_ANALYTICS_ID=G-XXXXXXXXXX
```

## Notes

- SQLite is used automatically for development unless `DJANGO_DB_ENGINE=postgresql` is set.
- The default email backend is Django's console backend, so password reset and contact/event emails print to the terminal during development.
- Demo content is created by `core/migrations/0002_seed_content.py`.
- Platform content is created by `academy/migrations/0002_seed_platform.py`.
- Uploaded media files are stored in `media/`.
- Static files are stored in `static/`; production deployments should run `python manage.py collectstatic`.
