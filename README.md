<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/matrimony-logo-light.svg">
  <img src="docs/assets/matrimony-logo.svg" alt="matrimony" width="440" height="120">
</picture>

# Your very own wedding website!

A beautiful, easy-to-deploy wedding website for you and your partner. Guests can save the date, confirm their RSVP, and take part in a wedding-day photo challenge - all managed through a simple admin panel, no config files required after setup.

## Screenshots

| Home | Details |
|------|---------|
| ![Home page](docs/screenshots/home.png) | ![Details page](docs/screenshots/details.png) |

| Photo Challenge | Gallery |
|-----------------|---------|
| ![Photo challenge](docs/screenshots/photo-challenge.png) | ![Gallery](docs/screenshots/gallery.png) |

| Admin Dashboard | Wedding Settings |
|-----------------|-----------------|
| ![Admin dashboard](docs/screenshots/admin-dashboard.png) | ![Wedding settings](docs/screenshots/admin-wedding.png) |

## Features

- **Wedding pages** for home, details, and live stream
- **Simple admin panel** - manage everything from the browser after first login
- **Save the Date** form to collect guest contact details before the big day
- **Personalised RSVP links** - each guest gets a unique QR code for one-click confirmation
- **Time-locked photo challenge** that unlocks automatically on your wedding day
- **Photo gallery** of guest-submitted challenge photos, downloadable as a ZIP
- **Email notifications** when guests save the date or confirm their RSVP
- **Customisable themes** - choose from classic, editorial, minimal, romantic, or luxe layouts with full colour control
- Optional **site password** to keep guest pages private until you're ready to share

---

## Deploy

### Option 1 - Render (free, one-click)

Render hosts the app and provisions a free PostgreSQL database automatically. No config needed — just connect your GitHub account.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/YOUR_REPO)

> **Before clicking:** push this repo to GitHub, then replace `YOUR_USERNAME/YOUR_REPO` in the badge link above with your actual GitHub path. Render reads `render.yaml` from the repo and sets everything up automatically — including the database and a random `SECRET_KEY`.

> **Note on photo uploads:** Render's free web service uses ephemeral storage, so uploaded photos won't survive a restart. This is fine for trying things out; for a real wedding event use the Docker option below or upgrade to a Render paid plan with a persistent disk.

### Option 2 - Docker

Spins up the app and a MariaDB container together. Requires [Docker](https://docs.docker.com/get-docker/) and Docker Compose.

```bash
cp .env.example .env
# Open .env and set SECRET_KEY to a long random string.
# The database is handled for you - no other changes needed.

docker compose up -d
```

Open `http://localhost:8000` in your browser. On first run you'll be walked through a short setup wizard.

**Using your own existing database?** Use the alternative compose file instead:

```bash
# Fill in DB_HOST, DB_USER, DB_PASS, DB_NAME (and optionally DATABASE_URL) in your .env
docker compose -f docker-compose.external-db.yml up -d
```

### Option 3 - Manual / venv (self-hosted)

For running directly on a server or your local machine with an existing MariaDB/MySQL instance.

**1. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment**

```bash
cp .env.example .env
```

Open `.env` and fill in:
- `SECRET_KEY` - any long random string (generate one with `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` - your database connection details

**4. Set up the database**

If you need to create the database and user from scratch:

```bash
python setup_database.py
```

If the database already exists and you just need to create the tables:

```bash
python setup_database.py --tables-only
```

**5. Run the app**

```bash
python app.py
```

Open `http://localhost:5000`. The setup wizard will appear on first run to create your admin account and enter your wedding details.

**Running in production?** Use Gunicorn instead:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## Admin Panel

Once you're set up, log in at `/admin` to manage everything from the browser - no config files or server restarts needed:

- **Wedding details** - couple names, date & time, venue info, registry links, Twitch stream
- **Theme & colours** - 5 layout styles and full colour customisation
- **Photo challenges** - add, edit, or remove challenges for your guests
- **Guest list** - view RSVPs, import/export CSV, send bulk emails
- **Photo gallery** - browse and download everything guests submitted
- **Site settings** - password protection and email (SMTP) configuration

---

## Tech Stack

- **Backend:** Flask, Flask-Mail, Flask-SQLAlchemy
- **Database:** MariaDB/MySQL
- **Frontend:** Jinja2 templates, custom CSS, vanilla JavaScript

---

## AI Disclaimer

Development of this site made heavy use of AI (Claude Sonnet 4.6) to take it from a custom and highly specific site for myself and my wife to something generic enough for anyone to use. The original site had no admin panel and was driven purely by database entries and YAML config files.
