# Generic Wedding Website - AI Coding Instructions

## Project Overview
Flask-based wedding website with photo challenge feature, live stream integration, and contact form. Features time-locked content that unlocks on the wedding day.

## Architecture

### Backend: Flask + SQLAlchemy + MySQL
- **`app.py`**: Single-file Flask application (no blueprint architecture)
- **Database**: MariaDB/MySQL via PyMySQL connector
- **Models**: `ChallengeAssignment` (guest→challenge mapping), `PhotoSubmission` (uploaded photos with metadata)
- **Config**: YAML-based (`config.yml`) - single source of truth for wedding details, email, database, challenges

### Frontend: Server-rendered Jinja2 + Vanilla JS
- **Templates**: Jinja2 inheritance via `base.html` (navbar, footer, flash messages)
- **Styling**: CSS custom properties (see `:root` in `style.css` for theming: `--primary-color`, `--secondary-color`)
- **No framework**: Pure JavaScript for interactivity (mobile nav, flash messages, lightbox, countdowns)

## Critical Workflows

### Development Setup
```bash
# 1. Virtual environment + dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Config setup
cp config.example.yml config.yml  # Edit with real credentials

# 3. Database initialization (interactive - prompts for root password)
python setup_database.py  # Creates DB, user, grants privileges

# 4. Run development server
python app.py  # Listens on 0.0.0.0:5000, debug=True
```

### Production Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Key Patterns & Conventions

### 1. Time-Locked Features (Wedding Day Mechanism)
```python
# Central pattern used across photo_challenge, gallery, stream routes
wedding_datetime = datetime.strptime(config['wedding']['date_full'], '%Y-%m-%d %H:%M:%S')
is_unlocked = datetime.now() >= wedding_datetime
```
- Photo challenges and gallery **hidden until `date_full` datetime** in config
- Frontend shows countdown timers that auto-reload when unlocked
- API endpoints (`/api/get-challenge`, `/api/upload-photo`) enforce with 403 responses

### 2. Configuration-Driven Content
**All wedding content lives in `config.yml`** - never hardcode:
- Wedding info: `config['wedding']['bride']`, `['groom']`, `['venue']`
- Challenge list: `config['photo_challenges']` (random assignment)
- Email settings: `config['mail']` (Gmail + app passwords)
- Twitch stream: `config['twitch']['channel']`
- **Site protection**: `config['site_protection']['enabled']` + `['password']` for optional password gate

When adding features, extend `config.yml` and update `config.example.yml` template.

### 3. Site Password Protection
```python
# Optional site-wide password protection via session-based authentication
@require_site_password  # Decorator checks config['site_protection']['enabled']
def protected_route():
    return render_template('page.html')
```
- Enable/disable: `config['site_protection']['enabled']` (boolean)
- Set password: `config['site_protection']['password']` (plaintext in config)
- Session persists via `session['site_authenticated']` after successful login
- All routes decorated with `@require_site_password` redirect to `/site-login` when locked
- Login template: `templates/site_login.html`

### 4. Database Session Management
```python
# Flask-SQLAlchemy auto-handles sessions - no manual commit needed unless:
assignment = ChallengeAssignment(guest_name=name, challenge=challenge)
db.session.add(assignment)
db.session.commit()  # Required for writes
```
- Tables auto-created via `db.create_all()` in `with app.app_context()` block
- Unique constraint on `ChallengeAssignment.guest_name` prevents duplicate challenges

### 5. File Upload Pattern
```python
# Photos saved to static/uploads/photos/ with timestamped, sanitized names
filename = f"{safe_name}_{timestamp}_{secure_filename(file.filename)}"
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
```
- 16MB limit via `MAX_CONTENT_LENGTH`
- Allowed extensions: `{'png', 'jpg', 'jpeg', 'gif'}`
- Upload folder created on startup: `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`

### 6. Dual Form Submission Support
Routes support both traditional POST (with `flash()` + `redirect()`) and AJAX (`/api/*` endpoints return JSON):
```python
@app.route('/contact', methods=['GET', 'POST'])  # Traditional form
@app.route('/api/contact', methods=['POST'])      # AJAX alternative
```

### 7. Frontend Styling Conventions
- **CSS Variables**: Theme colors in `:root` - modify `--primary-color` (#2d5016 green) for site-wide changes
- **Responsive**: Mobile-first grid layouts (`grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))`)
- **Fonts**: Cormorant Garamond (headings), Montserrat (body) from Google Fonts
- **No CSS framework** - custom utility classes (`.btn`, `.container`, `.page-header`)

## Integration Points

### Email (Flask-Mail)
- **Gmail setup requires app passwords** (2FA enabled) - document in config comments
- Contact form sends to `config['mail']['contact_email']`
- Error handling: catch exceptions, flash user-friendly messages

### Twitch Live Stream
- Embedded via `templates/stream.html` using channel from `config['twitch']['channel']`
- Toggle with `config['twitch']['enabled']`

### Photo Challenge System
1. Guest enters name → API checks `ChallengeAssignment` table
2. If new guest → assign random challenge from `config['photo_challenges']`, persist to DB
3. Guest uploads photo → saved to filesystem + `PhotoSubmission` record
4. Gallery displays all submissions with lightbox viewer

## Testing & Debugging

### Database Inspection
```bash
mysql -u wedding_user -p wedding_db
# Check tables: SHOW TABLES;
# View assignments: SELECT * FROM challenge_assignments;
```

### Photo Upload Testing
- Check filesystem: `ls static/uploads/photos/`
- Verify DB entries: `SELECT * FROM photo_submissions;`

### Date/Time Testing
**To test time-locked features without waiting:**
Temporarily modify `config.yml`:
```yaml
date_full: "2024-01-01 00:00:00"  # Past date to unlock immediately
```

## Common Gotchas

1. **Secret Key**: `config['flask']['secret_key']` must be set for sessions/flashing to work
2. **Database Connection**: Ensure MariaDB service running (`sudo systemctl start mariadb`)
3. **Upload Permissions**: `static/uploads/photos/` needs write permissions for web server user
4. **Email 535 Error**: Gmail blocking - use app-specific password, not account password
5. **Template Changes**: Flask auto-reloads in debug mode, but check browser cache for CSS/JS updates

## File Structure Reference
```
app.py                          # Single Flask app (routes + models + config)
config.yml                      # All customizable content (gitignored)
config.example.yml              # Template for config setup
setup_database.py               # One-time DB initialization script
templates/base.html             # Master layout (nav, footer, flash messages)
templates/rsvp.html             # RSVP form (no nav link, QR code access)
templates/rsvp_admin.html       # Password-protected RSVP table view
templates/photo_challenge.html  # Challenge assignment + upload UI
templates/gallery.html          # Photo grid with lightbox
static/css/style.css            # Theme variables + component styles
static/js/script.js             # Mobile nav, flash dismiss, smooth scroll
static/uploads/photos/          # User-uploaded challenge photos (gitignored)
```

## RSVP System

### How It Works
- **RSVP Form**: `/rsvp` route - NOT in navbar, accessed via QR code
- **Fields**: Names, Phone, Address, Email (all required)
- **Submission Flow**:
  1. Guest fills form → saved to `RSVPSubmission` model
  2. Email sent to `config['mail']['contact_email']` with submission details
  3. Email includes link to `/rsvp/admin` and password
  4. Success message flashed to user

### Admin View
- **URL**: `/rsvp/admin?password=<password>`
- **Authentication**: Query parameter password matches `config['site_protection']['password']`
- **Display**: Responsive table of all submissions with stats
- **Features**: Sortable by submission date, mailto links, print-friendly

### Database Model
```python
class RSVPSubmission(db.Model):
    names = db.Column(db.String(500))   # Multiple guest names
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
```

## Adding New Features

### New Routes
Add after existing routes in `app.py`, follow pattern:
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html', data=config['new_section'])
```
Update `templates/base.html` navbar with new link.

### New Database Tables
1. Define model class in `app.py` above existing models
2. Tables auto-created on next `python app.py` run (Flask-SQLAlchemy handles migrations for simple changes)
3. For complex migrations, consider Flask-Migrate

### New Config Options
1. Add to `config.yml` and `config.example.yml`
2. Access via `config['section']['key']` in routes
3. Pass to templates as context: `render_template('page.html', setting=config['setting'])`
