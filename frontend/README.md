# Clinic Staff Dashboard - Frontend

React-based web dashboard for clinic staff and doctors to manage appointments.

## Prerequisites

- Node.js (v18 or higher)
- Backend API running on `http://localhost:5000`

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will run on `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

The build files will be in the `dist/` directory.

## Features

### Dashboard
- Real-time appointment summary (total, completed, pending, etc.)
- Doctor-wise breakdown (staff/admin only)
- Live queue display with auto-refresh every 15 seconds
- WhatsApp appointment indicators

### Appointments
- Filter by date, doctor, and status
- View all appointment details
- Update appointment status with workflow validation
- WhatsApp/Manual source indicators
- Quick actions menu

### Role-Based Access
- **Admin**: Full access to all features
- **Staff**: View all appointments, manage appointments
- **Doctor**: View only their own appointments, update status

## Login Credentials (Demo)

- **Admin**: `admin` / `admin123`
- **Staff**: `staff` / `staff123`
- **Doctor**: `dr.sarah` / `doctor123`

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   │   └── MainLayout.jsx    # Sidebar + Header layout
│   │   └── ProtectedRoute.jsx    # Auth guard
│   ├── context/
│   │   └── AuthContext.jsx       # Authentication state
│   ├── pages/
│   │   ├── Login.jsx             # Login page
│   │   ├── Dashboard.jsx         # Main dashboard
│   │   └── AppointmentList.jsx   # Appointments table
│   ├── services/
│   │   └── api.js                # Axios instance
│   ├── App.jsx                   # Main app component
│   └── main.jsx                  # Entry point
├── index.html
├── vite.config.js
└── package.json
```

## Technologies Used

- **React 18** - UI library
- **Material UI** - Component library
- **React Router** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool

## API Integration

The frontend connects to the backend API at `/api/*` (proxied through Vite).

All API requests include JWT token in the Authorization header.

## Auto-Refresh

The queue display automatically refreshes every 15 seconds to show real-time updates.
