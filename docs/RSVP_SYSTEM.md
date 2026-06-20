# Save the Date & RSVP System

## Overview

The website now features a two-stage RSVP system:

### Stage 1: Save the Date
Guests visit the `/rsvp` page and enter their details:
- Name(s)
- Phone number
- Mailing address
- Email address

When they submit, the system:
- Saves their information to the database
- Generates a unique code for them
- Sends an admin notification email with their unique RSVP link

### Stage 2: RSVP Confirmation
Later, when you're ready to send formal invitations:
1. Each guest will receive their unique QR code/link
2. The link format is: `/rsvp/confirm/<unique_code>`
3. When they visit the link, they'll see their saved information
4. They can confirm their attendance with one click
5. The admin dashboard will update to show they've confirmed

## Admin Dashboard

Access at `/rsvp/admin/login` (requires site password)

The admin dashboard shows:
- List of all guests who submitted Save the Date info
- Their contact details
- Unique code for each guest
- RSVP confirmation status (✓ Yes or ⏳ Pending)
- Link to each guest's confirmation page
- Statistics: Total Guests, Confirmed RSVPs, Pending RSVPs

### Features:
- **Export to CSV**: Download all guest data including RSVP status
- **View Confirmation Links**: Click to see each guest's unique RSVP page
- **Real-time Status**: See who has confirmed instantly

## Database Schema

The `rsvp_submissions` table includes:
- `id`: Primary key
- `names`: Guest name(s)
- `phone`: Phone number
- `address`: Mailing address
- `email`: Email address
- `unique_code`: Unique URL-safe token (8 characters)
- `rsvp_confirmed`: Boolean (True/False)
- `rsvp_confirmed_at`: Timestamp when RSVP was confirmed
- `created_at`: Timestamp when Save the Date was submitted

## How to Use

### For Guests:
1. **Save the Date**: Visit `/rsvp` to submit contact information
2. **RSVP**: Later, scan the QR code on your invitation or click the link to confirm attendance

### For Admins:
1. Log in at `/rsvp/admin/login`
2. View all guest submissions
3. Copy unique RSVP links to include in invitations (or generate QR codes from them)
4. Track who has confirmed their RSVP
5. Export data to CSV for mail merge or other purposes

## Migration

The database schema was updated using `migrate_rsvp_table.py`. This script:
- Adds new columns: `unique_code`, `rsvp_confirmed`, `rsvp_confirmed_at`
- Generates unique codes for existing records
- Preserves all existing guest data

## Email Notifications

The system sends two types of emails to admins:

1. **Save the Date Submission**: When a guest submits their contact info
   - Includes their details
   - Provides their unique RSVP confirmation link

2. **RSVP Confirmation**: When a guest confirms their attendance
   - Notifies you that they've confirmed
   - Includes timestamp of confirmation

## QR Code Generation

To create QR codes for invitations:
1. Log into admin dashboard
2. Copy each guest's unique RSVP link
3. Use a QR code generator (e.g., qr-code-generator.com) to create codes
4. Include the QR code on their physical invitation

Alternatively, you could add a QR code generation feature to the admin page in the future.

## Security

- All admin pages require password authentication via session
- Unique codes are URL-safe random tokens (using Python's `secrets` module)
- Each code is guaranteed to be unique in the database
- RSVP links only work for the specific guest they're generated for
