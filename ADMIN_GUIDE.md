# Admin Guide - Wedding App

This guide explains how to use the admin control panel to manage your wedding website.

## Getting Started

### First Access - Setup Wizard

When you visit http://localhost:5000/admin/setup for the first time:

**Step 1: Create Admin Account**
- Email address (use a valid email)
- Password (at least 8 characters recommended)
- Click "Create Admin Account"

**Step 2: Enter Wedding Information**
- Couple names (bride & groom)
- Wedding date and year
- Venue name and city
- Click "Save Wedding Information"

**Step 3: Success**
- Your account is ready
- Visit http://localhost:5000/admin/login to continue

### Regular Login

1. Go to http://localhost:5000/admin/login
2. Enter your email and password
3. Click "Login"
4. You'll see the admin dashboard

## Admin Dashboard

The main admin page shows:
- **Total RSVPs** - How many guests have registered
- **Confirmed RSVPs** - How many have confirmed attendance
- **Photo Submissions** - Photos uploaded by guests
- **Photo Challenges** - Active challenges available
- **Quick Links** - Navigate to other admin sections

## Wedding Settings

Navigate to: **Dashboard** → **Wedding Settings** (gear icon)

### Section 1: Couple Information
- **Bride Name** - Displayed on homepage and emails
- **Groom Name** - Displayed on homepage and emails

### Section 2: Wedding Details
- **Wedding Date** - Date shown on website (e.g., "October 15, 2026")
- **Wedding Year** - Year on homepage hero (extracted from date)
- **Main Venue** - Primary venue name
- **City** - City/location

### Section 3: Event Locations & Times
- **Ceremony Location** - Address or room details (shown on /details)
- **Ceremony Time** - Start time (e.g., "4:00 PM")
- **Reception Location** - After ceremony venue
- **Reception Time** - Start time
- **After Party Location** (optional) - Late-night hangout spot

### Section 4: Theme Colors
Use the color pickers to customize the website appearance:
- **Primary Color** - Main theme color (buttons, headings)
- **Accent Color** - Secondary highlights
- **Gold Accent** - Luxury accents

**Note:** Color changes appear throughout the website immediately after saving.

### Section 5: Site Information
- **Site Title** - Browser tab title and emails
- **Domain** - Your website domain (used in QR code links)
- **Twitch Channel** (optional) - Channel name for live stream (e.g., "mywedding")
- **Enable Twitch** - Toggle live stream on/off

### Section 6: Site Protection
- **Protect Site with Password** - Checkbox to enable/disable
- **Site Password** - If enabled, guests must enter this password to access website
- **Use Case:** For pre-wedding access control

**To Save Changes:**
1. Scroll to bottom
2. Click "Save Changes" button
3. Look for green success message

## Managing Photo Challenges

Navigate to: **Dashboard** → **Challenges** (camera icon)

### Add a New Challenge

1. In the form at the top, enter:
   - **Challenge Name** - What guests will see (e.g., "Most Creative Dance Pose")
   - **Description** - Details about the challenge (optional)
2. Click "Add Challenge"
3. New challenge appears in the table below

### Challenge Assignment

Guests visiting `/photo-challenge`:
1. Enter their name
2. Receive a random, unique challenge
3. Upload a photo fulfilling that challenge
4. All guests see all challenges in the gallery

### Delete a Challenge

1. Click the red "Delete" button next to any challenge
2. This challenge won't be assigned to new guests (existing photos remain)

### Sample Challenges

Here are some ideas:
- "Most Creative Dance Pose"
- "Silliest Group Photo"
- "Best Dressed Guest"
- "Happiest Moment"
- "Best Sunset Shot"
- "Most Unexpected Location"

## RSVP Management

Navigate to: **Dashboard** → **RSVPs** (checklist icon)

### View Guest Registrations

The table shows all guests who filled out "Save the Date":
- **Names** - Guest names
- **Email** - Click to email them
- **Phone** - Contact number
- **Status** - "Confirmed" or "Pending"
- **Submitted** - Date they registered

### Statistics
- **Total Guests** - All registrations
- **Confirmed** - Guests who said yes
- **Pending** - Haven't confirmed yet

### Export Data

To export as CSV (for external tools like Excel):
```bash
# Coming in future version
# For now, copy/paste from the table
```

## Photo Gallery Management

Navigate to: **Dashboard** → **Gallery** (picture icon)

### View Submitted Photos

Table shows:
- **Guest Name** - Who submitted
- **Challenge** - Which challenge they fulfilled
- **Photo** - Click to view the image
- **Submitted** - Date received

### Delete a Photo

1. Find the photo in the table
2. Click the trash icon or delete button
3. Photo is removed from gallery

**Note:** Guests can still see deleted photos (they remain in the `/gallery` for guests to browse).

### Download Photos

1. Right-click on the photo thumbnail
2. Select "Save image as..."
3. Download to your computer

## Advanced Admin Tasks

### Sending Bulk Emails

**Note:** This feature is not yet in the UI. You can:
1. Access the RSVP list
2. Copy email addresses
3. Use your email client to send messages

### Resetting Passwords

If you forget your admin password:
1. Access MySQL/MariaDB directly
2. Reset the password using a script (ask developer)
3. Or recreate the admin account by clearing the database

### Modifying Guest Data

**Note:** Direct guest data editing coming in future version. For now:
1. Access MySQL directly (for technical users)
2. Or ask guests to re-register

### Accessing Database Directly

For advanced users:
```bash
mysql -u wedding_user -p wedding_db
# View all wedding configs: SELECT * FROM wedding_config;
# View RSVPs: SELECT * FROM rsvp_submissions;
# View photos: SELECT * FROM photo_submissions;
```

## Troubleshooting

### Forgot Admin Password

Option 1: Reset using MySQL (if technical):
```bash
mysql -u wedding_user -p wedding_db
DELETE FROM admin_user WHERE email='your@email.com';
# Then re-run setup wizard at /admin/setup
```

Option 2: Recreate the account via setup wizard:
```bash
# Clear the database (nuclear option)
# Then run /admin/setup again
```

### Color Changes Not Showing

1. Clear browser cache: Ctrl+Shift+Delete (Ctrl+Cmd+Delete on Mac)
2. Do a hard refresh: Ctrl+Shift+R
3. Try a different browser

### Challenges Not Showing on Public Site

Possible causes:
1. Wedding date hasn't arrived yet (features are time-locked)
2. No challenges added yet (add one in admin)
3. Clear browser cache

To test without waiting for wedding day:
1. Edit wedding date to today's date
2. Save changes
3. Refresh public site

### Emails Not Sending

Check:
1. Is email configured in Wedding Settings (mail settings in database)?
2. Is Gmail allowing access (app password enabled)?
3. Are there any error messages in logs?

## Tips & Best Practices

### 1. Use Descriptive Challenge Names
✅ Good: "Best Dance Floor Moment"
❌ Bad: "Photo 1"

### 2. Plan Challenge Names in Advance
- Create all challenges before the wedding
- Guests see all active challenges
- Too many = overwhelming; 3-5 is ideal

### 3. Test Site Features
Before wedding day:
1. Visit /rsvp as a guest and register
2. Check the confirmation email
3. Visit /photo-challenge and test upload
4. Verify photos appear in gallery

### 4. Backup Your Database
```bash
mysqldump -u wedding_user -p wedding_db > backup.sql
```

### 5. Set Up Site Password Close to Wedding Day
- Keep site public until 1 week before
- Then enable password protection
- Share password with invited guests only

### 6. Colors & Branding
- Test colors on mobile (they look different)
- Use high contrast between primary and background
- Gold accent works best sparingly

## Getting Help

### Common Questions

**Q: How do I add a second admin user?**
A: Not yet supported. Coming in future version.

**Q: Can guests edit their RSVP?**
A: Not yet supported. They can email or call you to change.

**Q: How do I delete all photos?**
A: Delete them one by one, or ask a developer to clear the database.

**Q: Can I schedule challenges to appear on specific dates?**
A: Not yet. All active challenges are available to all guests.

### Contacting Support

For technical issues:
1. Check SETUP.md for troubleshooting
2. Review Flask documentation
3. Contact your developer/IT support

---

**Happy wedding planning!** 🎉
