# Render.com Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `balichak-suman/appointment-booking`
3. Configure the service:
   - **Name**: `appointment-booking-bot` (or your choice)
   - **Region**: Choose closest to you (e.g., Singapore)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

### 3. Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"** and add these:

```
PORT=5000
WHATSAPP_API_URL=https://graph.facebook.com/v21.0
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
VERIFY_TOKEN=your_verify_token
GROQ_API_KEY=your_groq_api_key
```

**Copy these from your `.env` file!**

### 4. Add Google Credentials
You need to add your `credentials.json` file:

**Option A: Environment Variable (Recommended)**
1. Copy the entire content of your `credentials.json`
2. Add as environment variable:
   - **Key**: `GOOGLE_CREDENTIALS`
   - **Value**: Paste the entire JSON content

**Option B: Upload via Render Dashboard**
1. After deployment, use Render Shell
2. Upload `credentials.json` to the project root

### 5. Deploy!
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. You'll get a URL like: `https://appointment-booking-bot.onrender.com`

---

## 📝 Update WhatsApp Webhook

Once deployed, update your webhook URL:

1. Go to [Meta Developer Console](https://developers.facebook.com)
2. Your App → **WhatsApp** → **Configuration**
3. Click **"Edit"** next to Webhook
4. **Callback URL**: `https://your-app-name.onrender.com/webhook`
5. **Verify Token**: (same as your `VERIFY_TOKEN`)
6. Click **"Verify and Save"**
7. Subscribe to **messages** webhook field

---

## ✅ Verify Deployment

Test your webhook:
```bash
curl https://your-app-name.onrender.com/webhook
```

Should return: `{"status": "Webhook is active"}`

---

## 🔧 Troubleshooting

### Deployment Fails
- Check **Logs** in Render dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies

### Webhook Not Working
- Verify webhook URL is correct (must be HTTPS)
- Check verify token matches
- View logs in Render dashboard

### Google Calendar Not Working
- Ensure `GOOGLE_CREDENTIALS` environment variable is set
- Or upload `credentials.json` via Render Shell

---

## 📊 Monitor Your App

- **Logs**: Render Dashboard → Your Service → Logs
- **Metrics**: View CPU, Memory usage
- **Auto-deploy**: Pushes to `main` branch auto-deploy

---

## 🎯 Important Notes

1. **Free tier sleeps after 15 min inactivity**
   - First message takes ~30 sec to wake up
   - Stays awake during active conversations

2. **Data persistence**
   - `data/appointments.json` is ephemeral on free tier
   - Consider using a database for production

3. **Auto-deploys**
   - Every push to `main` triggers deployment
   - Takes 2-3 minutes

---

## 🔗 Your Deployment Checklist

- [ ] Create Render account
- [ ] Create new web service
- [ ] Add all environment variables
- [ ] Add Google credentials
- [ ] Deploy and get URL
- [ ] Update WhatsApp webhook
- [ ] Test with a message
- [ ] Monitor logs

---

**Need help?** Check Render logs or contact support!
