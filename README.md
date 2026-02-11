# Medical Dashboard & WhatsApp Appointment Bot 🏥

A complete Hospital Management System featuring a **Modern React Dashboard** and an **Advanced WhatsApp Bot** for automated appointments.

## 🌟 Key Features

### 🤖 WhatsApp Bot (Integrated)
- **Smart Booking**: Natural language date parsing (e.g., "Book for tomorrow at 5pm").
- **Real-time Availability**: Checks doctor's schedule instantly.
- **Google Calendar Sync**: 2-way sync for doctors; prevents double-booking.
- **Full Management**: Book, Reschedule, and Cancel appointments directly from WhatsApp.

### 💻 Admin Dashboard (React)
- **Doctor Management**: specialized views for managing doctor profiles.
- **Appointment Overview**: Validated grid view of all hospital bookings.
- **Patient Records**: Centralized patient database.

---

## 🛠️ Tech Stack

### Backend (`/backend`)
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Production-ready)
- **Services**: Meta Cloud API (WhatsApp), Google Calendar API, Groq AI.

### Frontend (`/frontend`)
- **Framework**: React.js + Vite
- **UI**: TailwindCSS (Modern & Responsive)

### Deployment
- **Platform**: Render.com (Monorepo support)
- **Infrastructure**: Web Service (API) + Static Site (Frontend) + Managed PostgreSQL.

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Configure .env (see backend/.env.example)
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Deployment (Render.com)
The project is configured for Render.
1.  **Connect Repo**: `balichak-suman/appointment-booking`.
2.  **Blueprints**: Render will auto-detect `render.yaml` and create:
    - `hospital-backend` (API + Bot)
    - `hospital-frontend` (UI)
    - `hospital-db` (PostgreSQL)

---

## 📂 Project Structure

```
├── backend/                # FastAPI Application & Bot Logic
│   ├── medical_backend/    # Main App Logic
│   ├── api/                # API Endpoints
│   ├── whatsapp_bot/       # Core Bot "Brain" (AI, Calendar, WhatsApp)
│   └── database.py         # Database Models
├── frontend/               # React Admin Dashboard
│   ├── src/                # UI Source Code
│   └── public/             # Static Assets
└── render.yaml             # Deployment Configuration
```

## 📄 License
MIT
