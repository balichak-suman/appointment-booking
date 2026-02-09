# Quick Start Guide

## What's New? 🎉

Your WhatsApp bot is now **production-ready** with:

✅ **5 Doctors** across 5 specializations (General Physician, Cardiologist, Dermatologist, Orthopedic, Pediatrician)  
✅ **Natural Language Dates** - Say "12th Feb", "tomorrow", "next Monday" instead of YYYY-MM-DD  
✅ **Smart Scheduling** - Only shows available time slots, prevents double-booking  
✅ **Complete Flow** - Specialization → Doctor → Date → Time → Confirmation

## How to Start

```bash
python app.py
```

Server runs on port **5000** (check your `.env` file)

## Example Conversation

**User:** "I need a doctor"  
**Bot:** Shows specializations (General Physician, Cardiologist, etc.)

**User:** "1" or "Cardiologist"  
**Bot:** Shows cardiologists with their availability

**User:** "1"  
**Bot:** "What date would you like? (tomorrow, 12th Feb, etc.)"

**User:** "12th Feb"  
**Bot:** Shows available time slots (09:00, 09:30, 10:00, etc.)

**User:** "3" or "10:00"  
**Bot:** "✅ Appointment Confirmed! ID: abc123, Dr. Michael Chen, 2026-02-12 at 10:00"

## Files Created

- `doctors_config.json` - Doctor database
- `doctor_service.py` - Availability management
- Enhanced `ai_service.py` - Natural date parsing
- Enhanced `app.py` - Complete conversation flow

## Important Note

Remember to add your phone number to Meta's **allowed list** in the developer console before testing!

## Customization

Edit `doctors_config.json` to:
- Add more doctors
- Change working hours
- Modify specializations
- Adjust slot duration
