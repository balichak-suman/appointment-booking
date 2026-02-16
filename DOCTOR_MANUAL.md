# 🩺 Doctor's Manual: Managing Your Schedule

This guide explains how to view your appointments and manage your availability using Google Calendar.

---

## 🔗 Link Google Calendar (Critical Step)
For the system to add appointments to your calendar, you **MUST** share it with our Service Account.

1.  **Create a New Calendar** (or use an existing one) in your Google Calendar.
2.  Go to **Settings and sharing** for that specific calendar.
3.  Scroll to **"Share with specific people or groups"**.
4.  Click **+ Add people and groups**.
5.  Paste this email address:
    `appointment-bot@airy-period-486906-a4.iam.gserviceaccount.com`
6.  Set permissions to **"Make changes to events"**.
7.  Click **Send**.
8.  Copy the **Calendar ID** (found near the bottom of settings) and paste it when adding a new doctor in the dashboard.

---

## 📅 Viewing Appointments

All appointments booked through WhatsApp will automatically appear in your **Google Calendar**.

### What You See
Each appointment event will include:
-   **Title**: `Appointment: [Patient Name]`
-   **Description**:
    -   Patient Name
    -   Phone Number
    -   Status (Confirmed)
-   **Time**: The specific booked slot (e.g., 10:00 AM - 10:30 AM).

---

## ⛔ Blocking Time Off

If you are unavailable for a specific time or day (e.g., vacation, lunch break, emergency), you can **block it directly in Google Calendar**.

1.  **Open Google Calendar**.
2.  **Create a New Event** for the time you want to block.
3.  **Title it "Busy"** (or anything else, the name doesn't matter).
4.  **Save** the event.

**Result**: The WhatsApp bot will instantly mark this time as **unavailable**, preventing patients from booking during this period.

---

## ⚙️ Changing Working Hours

Your standard working hours (e.g., Mon-Fri, 9 AM - 5 PM) are configured by the system administrator.

-   **To change your standard hours**: Contact the administrator.
-   **For temporary changes**: Use the "Blocking Time Off" method above.

---

## ❓ FAQ

**Q: Can I cancel a patient's appointment?**
A: Yes. If you delete the event from your Google Calendar, the slot becomes free again. However, it is recommended to contact the admin or have the patient cancel via WhatsApp to ensure they are notified.

**Q: What if I have a conflict?**
A: The system prevents double-booking. If you have a personal event in your calendar at 2 PM, the bot will not allow a patient to book at 2 PM.
