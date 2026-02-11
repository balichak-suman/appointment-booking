# 🚀 Manual Deployment Guide (Free Tier)

Follow these steps to deploy your application manually on Render.com to ensure you stay on the **Free Tier**.

## 1️⃣ Database (PostgreSQL)

1.  **Dashboard** → **New +** → **PostgreSQL**.
2.  **Name**: `hospital-db`.
3.  **Region**: Choose the one closest to you (e.g., `Singapore` or `Frankfurt`).
4.  **Instance Type**: Ensure **"Free"** is selected.
5.  **Create Database**.
6.  **Wait** for it to become "Available".
7.  **Copy the "Internal Database URL"** (starts with `postgres://...`). You will need this for the Backend.

---

## 2️⃣ Backend API (Web Service)

1.  **Dashboard** → **New +** → **Web Service**.
2.  **Connect Repo**: `balichak-suman/appointment-booking`.
3.  **Name**: `hospital-backend`.
4.  **Root Directory**: `backend` (Important!).
5.  **Runtime**: `Python 3`.
6.  **Build Command**: `pip install -r requirements.txt`.
7.  **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
8.  **Instance Type**: Select **"Free"**.
9.  **Environment Variables** (Click "Advanced"):
    *   `DATABASE_URL`: Paste the Internal Database URL from Step 1.
    *   `WHATSAPP_API_URL`: `https://graph.facebook.com/v21.0`
    *   `WHATSAPP_PHONE_NUMBER_ID`: (Your ID)
    *   `WHATSAPP_ACCESS_TOKEN`: (Your Token)
    *   `WHATSAPP_VERIFY_TOKEN`: (Your Verify Token)
    *   `GROQ_API_KEY`: (Your Key)
    *   `GOOGLE_CREDENTIALS`: (Content of `credentials.json`)
10. **Create Web Service**.
11. **Copy the Backend URL** (e.g., `https://hospital-backend.onrender.com`) once deployed.

---

## 3️⃣ Frontend UI (Static Site)

1.  **Dashboard** → **New +** → **Static Site**.
2.  **Connect Repo**: `balichak-suman/appointment-booking`.
3.  **Name**: `hospital-frontend`.
4.  **Root Directory**: `frontend`.
5.  **Build Command**: `npm install && npm run build`.
6.  **Publish Directory**: `dist`.
7.  **Environment Variables**:
    *   `VITE_API_URL`: Paste the Backend URL from Step 2.
8.  **Create Static Site**.

---

## 🎉 Done!
Your application is now live on the Free Tier!
-   **Backend**: Handles API & WhatsApp Bot.
-   **Frontend**: User Dashboard.
-   **Database**: Stores appointments & doctors.
