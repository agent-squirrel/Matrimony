# Your very own wedding website!

Flask-based wedding website, with configuration-driven content, optional site password protection, a time-locked photo challenge and gallery, and a two-stage save-the-date / RSVP workflow.

## Features

- **Wedding website pages** for the home page, details, and live stream
- **Optional site password protection** for guest-facing pages
- **Time-locked photo challenge** that unlocks on the wedding day
- **Photo gallery** backed by MySQL and filesystem uploads
- **Save the Date flow** that collects guest mailing details
- **Personalized RSVP confirmation links** using unique guest codes
- **Admin RSVP dashboard** with CSV export and printable QR code pages
- **Email notifications** for new submissions and RSVP confirmations

## Tech Stack

- **Backend:** Flask, Flask-Mail, Flask-SQLAlchemy
- **Database:** MariaDB/MySQL via PyMySQL
- **Frontend:** Jinja2 templates, custom CSS, vanilla JavaScript
- **Other integrations:** QR code generation with `qrcode`

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Home page |
| `/details` | Wedding details |
| `/stream` | Twitch live stream page |
| `/photo-challenge` | Wedding-day photo challenge |
| `/gallery` | Submitted photo gallery |
| `/save` | Save the Date form |
| `/rsvp/confirm/<code>` | Guest RSVP confirmation page |
| `/rsvp/admin/login` | RSVP admin login |
| `/rsvp/admin` | RSVP dashboard |
| `/rsvp/admin/export` | CSV export |
| `/rsvp/admin/qr-codes` | Printable guest QR codes |

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your config file

```bash
cp config.example.yml config.yml
```

Update `config.yml` with:

- `flask.secret_key`
- `database.*`
- `mail.*`
- `wedding.*`
- `details.*`
- `twitch.*`
- `site_protection.*`
- `photo_challenges`

### 4. Set up the database

```bash
python setup_database.py
```

### 5. Run the app

```bash
python app.py
```

The development server listens on `http://localhost:5000`.

## Configuration Notes

- `config.yml` is the source of truth for wedding content, mail settings, database credentials, stream settings, and photo challenges.
- `site_protection.enabled` controls whether guest-facing routes require the shared site password.
- `wedding.date_full` controls when the photo challenge and gallery unlock.
- Uploaded photos are stored in `static/uploads/photos/`.

## Save the Date and RSVP Flow

1. Guests submit their details at `/save`.
2. The app stores their record in `rsvp_submissions` and generates a unique code.
3. Admins manage entries through `/rsvp/admin`.
4. Guests later confirm attendance via `/rsvp/confirm/<code>`.
5. Admins can export data to CSV or print guest QR codes from the dashboard.

## Email Behavior

The app can send:

- notification emails when a guest submits the Save the Date form
- notification emails when a guest confirms their RSVP
- confirmation emails back to guests after RSVP confirmation

## Production

Run with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Project Structure

```text
app.py
config.example.yml
config.yml
setup_database.py
migrate_rsvp_table.py
templates/
static/
```

# AI Disclaimer
Development of this site made heavy use of AI (Claude Sonnet 4.6) to take it from a custom and highly specific site for myself and my wife to something generic enough for anyone to use.
The original site had no admin panel and was driven purely by database entries and YAML config files.
