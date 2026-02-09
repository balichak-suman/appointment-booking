# Google Calendar Setup Instructions

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project"
3. Name it "WhatsApp Appointment Bot"
4. Click "Create"

## Step 2: Enable Google Calendar API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and click "Enable"

## Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "appointment-bot-service"
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

## Step 4: Download Credentials

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON" format
5. Click "Create"
6. Save the downloaded file as `credentials.json` in your project folder:
   ```
   c:\Users\D-IT\Desktop\test\credentials.json
   ```

## Step 5: Share Calendars with Service Account

1. Open Google Calendar (calendar.google.com)
2. Create 3 calendars (one for each doctor):
   - "Dr. Sarah Johnson - Appointments"
   - "Dr. Michael Chen - Appointments"
   - "Dr. Priya Sharma - Appointments"

3. For each calendar:
   - Click the 3 dots next to the calendar name
   - Click "Settings and sharing"
   - Scroll to "Share with specific people"
   - Click "Add people"
   - Paste the service account email (from credentials.json, looks like: `appointment-bot-service@project-id.iam.gserviceaccount.com`)
   - Set permission to "Make changes to events"
   - Click "Send"

4. Get each calendar ID:
   - In calendar settings, scroll to "Integrate calendar"
   - Copy the "Calendar ID" (looks like: `abc123@group.calendar.google.com`)

## Step 6: Update doctors_config.json

Replace the `google_calendar_id` for each doctor with their actual calendar IDs:

```json
{
  "id": "dr_001",
  "name": "Dr. Sarah Johnson",
  "google_calendar_id": "PASTE_CALENDAR_ID_HERE",
  ...
}
```

## Step 7: Test

Run this command to test the connection:

```bash
python -c "from google_calendar_service import google_calendar_service; print('Service initialized:', google_calendar_service.service is not None)"
```

If it prints `Service initialized: True`, you're all set!

## Important Notes

- Keep `credentials.json` secure and never commit it to version control
- Add `credentials.json` to your `.gitignore` file
- The service account email needs "Make changes to events" permission on all doctor calendars
