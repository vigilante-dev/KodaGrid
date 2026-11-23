# KodaGrid Django Website

A professional, responsive technology education website for a coding academy or youth digital skills organization. The project uses Python, Django, Django templates, HTML5, and custom CSS only.

## Features

- Public pages for Home, About, Courses, Events, Blog, Gallery, and Contact.
- Django authentication for student registration, login, logout, profile, and password reset.
- Django Admin management for students, courses, events, event registrations, blog posts, testimonials, gallery items, newsletter subscribers, and contact messages.
- Signed-in learners can submit testimonials for admin review before publication.
- W3Schools-style learning paths for programming, web, mobile, databases, cloud, cybersecurity, and AI with lessons, exercises, quizzes, notes, and projects.
- Student portal with live progress, upcoming assignments, certificates, recommended paths, and mentorship activity.
- Google Classroom-style workspace with class-code joining, trainer/staff class creation, class streams, materials, attendance marking, assignment submissions, and grade feedback.
- Coding games with a weekly leaderboard built from signed-in players' saved scores.
- Admin-managed fee plans, trainer applications, mentorship bookings, resources, job opportunities, community challenges, and certificate verification records.
- Search and filtering for courses, events, and blog articles.
- SEO-friendly slug URLs for courses, events, and blog posts.
- Contact form, newsletter signup, CSRF protection, form validation, and console email notifications.
- Media upload support for course images, profile pictures, blog images, gallery images, and testimonials.
- Image analysis command that optimizes images, classifies educational relevance, generates captions, and recommends page placements.
- Pagination for listing pages.
- Optional Google Analytics hook through `DJANGO_ANALYTICS_ID`.
- Responsive Django templates with persistent light/dark themes, English, Swahili, French, and Portuguese UI translations, and theme-aware Lucide-style SVG icons; no frontend framework is required.
- The About page team section lists approved trainer profiles from the admin.
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
DATABASE_URL=postgresql://your-user:your-password@your-render-postgres-host:5432/your-database
DJANGO_DB_ENGINE=postgresql
POSTGRES_DB=your-render-database-name
POSTGRES_USER=your-render-database-user
POSTGRES_PASSWORD=replace-with-a-secure-password
POSTGRES_HOST=your-render-postgres-host
POSTGRES_PORT=5432
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=KodaGrid <webmaster@example.com>
CONTACT_EMAIL=your-inbox@example.com
DJANGO_ANALYTICS_ID=G-XXXXXXXXXX
```

The login and registration pages use Django authentication and Django sessions. Student accounts must be approved by an administrator before they can log in. Apply migrations after deployment so the latest account approval and private chat features are available.

Optional tuning:

```text
DJANGO_LOG_LEVEL=INFO                 # errors and tracebacks are written to stderr (Render logs)
DJANGO_MAX_IMAGE_UPLOAD_MB=5          # profile/registration photo size limit
DJANGO_TRUST_X_FORWARDED_FOR=True     # defaults to True on Render; used by the POST rate limiter
DJANGO_MEDIA_ROOT=/var/data/media     # point at a persistent disk so uploads survive deploys
```

Footer contact details and social profiles (each is hidden until set; social URLs must start with `https://`):

```text
PUBLIC_CONTACT_EMAIL=hello@example.com
PUBLIC_CONTACT_PHONE=+254 700 000 000
SOCIAL_LINKEDIN_URL=https://www.linkedin.com/company/...
SOCIAL_X_URL=https://x.com/...
SOCIAL_INSTAGRAM_URL=https://www.instagram.com/...
SOCIAL_YOUTUBE_URL=https://www.youtube.com/@...
SOCIAL_FACEBOOK_URL=https://www.facebook.com/...
```

## Deploying on Render

- **Build command:** `./build.sh` (installs requirements, runs `collectstatic`, then `migrate`)
- **Start command:** `gunicorn config.wsgi:application`
- Set `DJANGO_SECRET_KEY` and `DATABASE_URL` in the dashboard. `DEBUG` turns off automatically when `RENDER_EXTERNAL_HOSTNAME` is present.
- **Uploaded media:** Render's filesystem is wiped on every deploy. Attach a persistent disk and set `DJANGO_MEDIA_ROOT` to a folder on it, otherwise gallery, course, and profile uploads disappear after each deploy.
- Media is served by Django with per-folder access rules (`core/media.py`): course, event, blog, gallery, trainer, and resource images are public; class materials and assignment attachments need a signed-in user; student photos, trainer CVs, and submissions are staff-only.

## Notes

- SQLite is used automatically for development unless `DATABASE_URL` or `DJANGO_DB_ENGINE=postgresql` is set.
- The default email backend is Django's console backend, so password reset and contact/event emails print to the terminal during development.
- Demo content is created by `core/migrations/0002_seed_content.py`.
- Platform content is created by `academy/migrations/0002_seed_platform.py`.
- Uploaded media files are stored in `media/`.
- Static files are stored in `static/` and served by WhiteNoise with hashed, compressed filenames after `collectstatic`.
- Render's `RENDER_EXTERNAL_HOSTNAME` is used automatically for allowed hosts and CSRF origins. Set the database, secret key, and mail environment variables in the Render dashboard.
- Private messages are stored in Django and restricted to their two participants. The shared tutor announcement room is readable by signed-in users and writable only by approved trainers or staff. Calls use Jitsi Meet; invite links are private conversation messages, while the meeting media is handled by Jitsi.
- When `DATABASE_URL` is set, it takes precedence over the separate `POSTGRES_*` settings.
