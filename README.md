# WhatsApp Appointment Booking Bot 🏥

A production-ready WhatsApp bot for hospital appointment booking, featuring Google Calendar integration, specialization filtering, and double-booking prevention.

## 🌟 Features

- **👩‍⚕️ Smart Booking Flow**:
  - Filter doctors by **Specialization** (Cardiologist, Dermatologist, etc.)
  - View doctor availability in real-time
  - Select dates using natural language (e.g., "tomorrow", "next Monday")
- **📅 Google Calendar Integration**:
  - 2-way sync with doctor calendars
  - Automatically creates events for new bookings
  - Prevents double-booking by checking Calendar busy slots
- **🛡️ Robust Validation**:
  - Prevents booking past time slots
  - Validates phone numbers and inputs
- **⚡ Interactive UI**: Uses WhatsApp List Messages and Buttons for a seamless experience.
- **🔄 Full Management**: Book, Reschedule, and Cancel appointments.

---

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **WhatsApp API**: Meta Cloud API (Graph API v21.0)
- **Database**: JSON-based local storage (Production: Switch to PostgreSQL/MongoDB)
- **Integrations**: Google Calendar API, Groq AI (for natural language parsing)
- **Deployment**: Render.com (Gunicorn)

---

## 🚀 Setup Guide

### 1. Prerequisites
- Python 3.8+
- Meta Developer Account (WhatsApp Business API)
- Google Cloud Project (for Calendar API)
- Groq API Key (for date parsing)

### 2. Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/balichak-suman/appointment-booking.git
    cd appointment-booking
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

Create a `.env` file in the root directory:

```env
PORT=5000
WHATSAPP_API_URL=https://graph.facebook.com/v21.0
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
VERIFY_TOKEN=your_verify_token
GROQ_API_KEY=your_groq_api_key
```

### 4. Google Calendar Setup

1.  **Create Service Account**:
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Create a project -> Enable "Google Calendar API".
    - Create a Service Account -> Download JSON key as `credentials.json`.
    - Place `credentials.json` in the project root (**Do not commit this file!**).

2.  **Share Calendars**:
    - Create a Google Calendar for each doctor.
    - Share each calendar with the Service Account email (Setting: "Make changes to events").
    - Get the **Calendar ID** for each (e.g., `abc1234@group.calendar.google.com`).

3.  **Update `doctors_config.json`**:
    - Add your doctors, specializations, and their Calendar IDs.

```json
{
  "doctors": [
    {
      "id": "dr_001",
      "name": "Dr. Sarah Johnson",
      "specialization": "General Physician",
      "google_calendar_id": "your_calendar_id_here",
      "working_hours": { "start": "09:00", "end": "17:00" },
      "slot_duration_minutes": 30
    }
  ]
}
```

---

## 🏃‍♂️ Running the Bot

### Local Development
```bash
python app.py
```
*Server runs on port 5000 (default).*

### Deployment (Render.com)
1.  **Create Web Service** on Render.
2.  **Connect Repo**: `balichak-suman/appointment-booking`.
3.  **Runtime**: Python 3.
4.  **Build Command**: `pip install -r requirements.txt`.
5.  **Start Command**: `gunicorn app:app`.
6.  **Environment Variables**: Add all variables from `.env`.
    - For `credentials.json`, either upload it via "Secret Files" or set a `GOOGLE_CREDENTIALS` env var with the file content.

7.  **Keep it Alive (Free Tier)**:
    - Render's free tier spins down after 15 minutes of inactivity.
    - To prevent this, use a free service like **[UptimeRobot](https://uptimerobot.com/)**.
    - Create a new HTTP monitor that pings your bot's URL (e.g., `https://your-app-name.onrender.com/webhook`) every 5-10 minutes.
    - This will keep your bot awake and responsive 24/7.

---

## 📱 Usage

1.  **Start Chat**: Send any message (e.g., "Hi", "Book appointment") to your WhatsApp number.
2.  **Select Option**: Choose "Book Appointment" from the menu.
3.  **Flow**:
    - Select **Specialization**.
    - Select **Doctor**.
    - Choose **Date** (e.g., "Tomorrow").
    - Choose **Time Slot**.
4.  **Confirmation**: Receive a booking confirmation with details.

---

## 📂 Project Structure

```
├── app.py                      # Main Flask application & Webhook entry
├── appointment_manager.py      # Core booking logic (CRUD)
├── doctor_service.py           # Doctor & Specialization management
├── google_calendar_service.py  # Google Calendar API wrapper
├── ai_service.py               # Groq AI integration for date parsing
├── whatsapp_client.py          # Meta Cloud API wrapper
├── config.py                   # Configuration loader
├── doctors_config.json         # Doctor data (Database)
├── data/                       # Local appointment storage
└── templates/ & static/        # (Optional) Web UI assets
```

## 🔧 Troubleshooting

-   **Webhook Error**: Ensure `VERIFY_TOKEN` matches in `.env` and Meta Dashboard.
-   **Calendar 403**: Ensure the calendar is shared with the Service Account email.
-   **"Past Time" Error**: The bot automatically filters out past time slots based on server time.

## 📄 License

MIT
