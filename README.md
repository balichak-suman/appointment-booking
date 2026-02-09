# WhatsApp Appointment Booking Bot

A production-ready WhatsApp bot for hospital appointment booking with Google Calendar integration.

## Features

- 📅 **Book Appointments** - Select specialization, doctor, date, and time
- ❌ **Cancel Appointments** - Cancel existing appointments
- 🔄 **Reschedule Appointments** - Change appointment date/time
- 📊 **Google Calendar Sync** - Automatic calendar integration
- 🔒 **Double-booking Prevention** - Checks local storage and Google Calendar
- ⏰ **Smart Time Validation** - Prevents booking past time slots
- 📱 **Interactive UI** - WhatsApp buttons and lists for seamless UX

## Tech Stack

- **Backend**: Python 3.x, Flask
- **WhatsApp**: Meta Cloud API
- **Calendar**: Google Calendar API
- **Storage**: JSON-based local storage

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
PORT=5000
WHATSAPP_API_URL=https://graph.facebook.com/v21.0
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
VERIFY_TOKEN=your_verify_token
GROQ_API_KEY=your_groq_api_key
```

### 3. Google Calendar Setup

1. Create a Google Cloud project
2. Enable Google Calendar API
3. Create a service account
4. Download `credentials.json` to project root
5. Share doctor calendars with service account email

### 4. Configure Doctors

Edit `doctors_config.json` with your doctors' information:

```json
{
  "doctors": [
    {
      "id": "dr_001",
      "name": "Dr. Sarah Johnson",
      "specialization": "General Physician",
      "google_calendar_id": "your_calendar_id@group.calendar.google.com",
      "working_hours": {
        "start": "09:00",
        "end": "17:00"
      },
      "slot_duration_minutes": 30
    }
  ]
}
```

### 5. Run the Server

```bash
python app.py
```

## Usage

1. Send any message to your WhatsApp bot
2. Choose from: Book | Cancel | Reschedule
3. Follow the interactive prompts
4. Receive confirmation with appointment details

## Project Structure

```
├── app.py                      # Main Flask application
├── appointment_manager.py      # Appointment logic
├── doctor_service.py          # Doctor management
├── google_calendar_service.py # Calendar integration
├── whatsapp_client.py         # WhatsApp API client
├── config.py                  # Configuration
├── doctors_config.json        # Doctor data
├── .env                       # Environment variables (not in git)
└── credentials.json           # Google credentials (not in git)
```

## License

MIT
