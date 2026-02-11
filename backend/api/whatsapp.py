"""
WhatsApp Integration Module for Medical Dashboard
Handles WhatsApp booking, cancellation, and rescheduling
Directly integrated into the FastAPI backend
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
import os
import traceback
import json
from whatsapp_bot.config import config

# Import local bot services
from whatsapp_bot.whatsapp_client import whatsapp_client
# from whatsapp_bot.ai_service import ai_service # AI Removed
from whatsapp_bot.doctor_service import doctor_service
from whatsapp_bot.appointment_manager import appointment_manager
from whatsapp_bot.google_calendar_service import google_calendar_service
from whatsapp_bot.cancel_functions import show_user_appointments, cancel_appointment

router = APIRouter(tags=["WhatsApp"])

# ==================== WEBHOOK ENDPOINTS ====================

@router.head("/webhook")
async def verify_webhook_head():
    """Handle HEAD requests for UptimeRobot/Meta"""
    return {"status": "ok"}

@router.get("/webhook")
async def verify_webhook(request: Request):
    """Verify WhatsApp webhook"""
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')
    
    # Use config
    VERIFY_TOKEN = config.WHATSAPP_VERIFY_TOKEN
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    
    return {"status": "ok", "message": "Webhook endpoint is active"}

@router.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive WhatsApp messages and process them"""
    try:
        data = await request.json()
        print(f"Webhook Received: {json.dumps(data)}")
        
        if data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    
                    if 'messages' in value:
                        for message in value['messages']:
                            # Process each message in background to avoid timeouts
                            background_tasks.add_task(process_message, message, value)
        
        return {"status": "EVENT_RECEIVED"}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

async def process_message(message, value):
    """Process a single WhatsApp message"""
    try:
        sender = message.get('from')
        message_type = message.get('type')
        
        # Extract sender name
        sender_name = "User"
        contacts = value.get('contacts', [])
        if contacts:
            sender_name = contacts[0].get('profile', {}).get('name', 'User')
        
        # Handle different message types
        if message_type == 'text':
            message_body = message.get('text', {}).get('body', '')
            await handle_incoming_message(sender, sender_name, message_body, None)
        
        elif message_type == 'interactive':
            interactive = message.get('interactive', {})
            interactive_type = interactive.get('type')
            
            if interactive_type == 'list_reply':
                selection_id = interactive.get('list_reply', {}).get('id')
                await handle_incoming_message(sender, sender_name, '', selection_id)
            
            elif interactive_type == 'button_reply':
                button_id = interactive.get('button_reply', {}).get('id')
                await handle_incoming_message(sender, sender_name, '', button_id)
                
    except Exception as e:
        print(f"Error in process_message: {e}")
        traceback.print_exc()

# ==================== CORE LOGIC ====================

async def handle_incoming_message(user_id: str, user_name: str, message_body: str, interaction_id: str):
    """Main message handler"""
    session = appointment_manager.get_session(user_id)
    step = session.get("step")
    
    print(f"Handling message from {user_name} ({user_id}). Step: {step}, Interaction: {interaction_id}")
    
    # If text message 'hi' or 'menu', reset
    if message_body and message_body.lower() in ['hi', 'hello', 'menu', 'start', 'restart']:
        send_main_menu(user_id, user_name)
        return

    # 1. Handle selection/button click
    if interaction_id:
        await process_interaction(user_id, user_name, interaction_id, session)
        return

    # 2. Handle simple text intent (Rule-based, no AI)
    if message_body:
        text = message_body.lower().strip()
        
        # Simple Keyword Matching
        if text in ['book', 'appointment', 'schedule', 'booking', 'new']:
            send_specialization_list(user_id)
            appointment_manager.update_session(user_id, {"step": "awaiting_specialization", "tempData": {"userName": user_name}})
        
        elif text in ['cancel', 'cancellation', 'delete', 'remove']:
            show_user_appointments(user_id)
            
        elif text in ['reschedule', 'change', 'move', 'update']:
            appointment_manager.update_session(user_id, {"step": "rescheduling"})
            show_user_appointments(user_id)
            
        else:
            # Default: Show Main Menu for any other text
            send_main_menu(user_id, user_name)

def send_main_menu(user_id: str, user_name: str):
    """Send the main menu buttons"""
    buttons = [
        {"id": "book_appointment", "title": "Book Appointment"},
        {"id": "reschedule_appointment", "title": "Reschedule"},
        {"id": "cancel_appointment", "title": "Cancel Appointment"}
    ]
    whatsapp_client.send_interactive_buttons(
        user_id,
        f"Hello {user_name}! Welcome to City Hospital. How can we help you today?",
        buttons
    )
    appointment_manager.update_session(user_id, {"step": "idle"})

async def process_interaction(user_id: str, user_name: str, interaction_id: str, session: dict):
    """Process button or list selection"""
    
    # Root buttons
    if interaction_id == "book_appointment":
        send_specialization_list(user_id)
        appointment_manager.update_session(user_id, {"step": "awaiting_specialization", "tempData": {"userName": user_name}})
        return
    
    if interaction_id == "cancel_appointment":
        show_user_appointments(user_id)
        return

    if interaction_id == "reschedule_appointment":
        # For now, rescheduling is just cancelling + booking. 
        # So we show appointments to cancel first.
        # Ideally, we should set a flag in session to know it's a reschedule flow.
        appointment_manager.update_session(user_id, {"step": "rescheduling"})
        show_user_appointments(user_id) 
        return
    
    # Specialization selection
    if interaction_id.startswith("spec_"):
        spec = interaction_id.replace("spec_", "")
        appointment_manager.update_session(user_id, {"step": "awaiting_doctor", "tempData": {**session["tempData"], "specialization": spec}})
        send_doctor_list(user_id, spec)
        return
    
    # Doctor selection
    if interaction_id.startswith("dr_") or interaction_id.isdigit():
        doctor_id = interaction_id.replace("dr_", "")
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if doctor:
            appointment_manager.update_session(user_id, {
                "step": "awaiting_date",
                "tempData": {
                    **session.get("tempData", {}),
                    "doctor_id": doctor['id'],
                    "doctor_name": doctor['name'],
                    "specialization": doctor['specialization']
                }
            })
            send_date_list(user_id, doctor['id'])
        return
    
    # Date selection
    if interaction_id.startswith("date_"):
        date = interaction_id.replace("date_", "")
        current_data = session.get("tempData", {})
        appointment_manager.update_session(user_id, {
            "step": "awaiting_time",
            "tempData": {**current_data, "date": date}
        })
        send_time_slots(user_id, current_data.get("doctor_id"), date)
        return
    
    # Time selection -> CONFIRM BOOKING
    if interaction_id.startswith("time_"):
        time = interaction_id.replace("time_", "")
        temp_data = session.get("tempData", {})
        
        # Validate Booking Constraints
        is_valid, error_msg, error_code = appointment_manager.validate_booking_constraints(
            user_id, 
            temp_data.get("doctor_id"), 
            temp_data.get("date"), 
            time
        )
        
        if not is_valid:
            if error_code == "SAME_DOCTOR_DAY":
                buttons = [
                    {"id": "reschedule_appointment", "title": "Reschedule Existing"},
                    {"id": f"date_{temp_data.get('date')}", "title": "Choose Different Date"} # Actually need to go back to date selection properly
                ]
                # Better to just offer Reschedule or Cancel
                buttons = [
                    {"id": "reschedule_appointment", "title": "Reschedule Old"},
                    {"id": "cancel_appointment", "title": "Cancel Old"}
                ]
                whatsapp_client.send_interactive_buttons(user_id, f"⚠️ {error_msg}", buttons)
                
            elif error_code == "TIME_CLASH":
                # Go back to time selection for this doctor/date
                # We can re-trigger time slots logic or just give a button to do so
                # But button IDs in WhatsApp are for interactions. 
                # Let's just send a message and then re-send the time slots?
                # Or better, a button "Choose Different Time" that triggers... logic?
                # Actually, simpler: Just send message and re-send time slots.
                whatsapp_client.send_message(user_id, f"⚠️ {error_msg}")
                send_time_slots(user_id, temp_data.get("doctor_id"), temp_data.get("date"))
                
            else:
                 whatsapp_client.send_message(user_id, f"⚠️ {error_msg}")
                 send_main_menu(user_id, user_name)
                 
            return

        # Create appointment in DB
        try:
            appointment = appointment_manager.create_appointment(
                user_id,
                temp_data.get("userName", user_name),
                temp_data.get("doctor_id"),
                temp_data.get("doctor_name"),
                temp_data.get("specialization"),
                temp_data.get("date"),
                time
            )
            
            # Google Calendar
            doctor = doctor_service.get_doctor_by_id(temp_data.get("doctor_id"))
            if doctor and google_calendar_service.service and doctor.get('google_calendar_id'):
                google_calendar_service.create_appointment(
                    doctor.get('google_calendar_id'), 
                    temp_data.get("userName", user_name), 
                    user_id,
                    temp_data.get("doctor_name"), 
                    temp_data.get("date"), 
                    time,
                    doctor.get('slot_duration_minutes', 30)
                )
            
            appointment_manager.clear_session(user_id)
            
            whatsapp_client.send_message(
                user_id, 
                f"✅ *Appointment Confirmed!*\n\n"
                f"ID: {appointment['id']}\n"
                f"Doctor: {temp_data.get('doctor_name')}\n"
                f"Date: {temp_data.get('date')}\n"
                f"Time: {time}\n\n"
                f"See you then!"
            )
        except Exception as e:
            whatsapp_client.send_message(user_id, f"Error booking appointment: {str(e)}")
            print(traceback.format_exc())
        return

    # Cancellation
    if interaction_id.startswith("cancel_"):
        # Format: cancel_ID or cancel_ID_index
        parts = interaction_id.split("_")
        if len(parts) >= 2:
            apt_id = parts[1]
            cancel_appointment(user_id, apt_id)
            
            # Check if we are in rescheduling mode
            current_step = session.get("step")
            if current_step == "rescheduling":
                whatsapp_client.send_message(user_id, "🗓️ Now, let's book your new appointment time.")
                send_specialization_list(user_id)
                appointment_manager.update_session(user_id, {"step": "awaiting_specialization", "tempData": {"userName": user_name}})
        return

# ==================== UI HELPERS ====================

def send_specialization_list(user_id: str):
    specs = doctor_service.get_all_specializations()
    rows = [{"id": f"spec_{s}", "title": s} for s in specs]
    sections = [{"title": "Our Departments", "rows": rows}]
    whatsapp_client.send_interactive_list(user_id, "Choose Department", "Select the type of care you need:", "View Departments", sections)

def send_doctor_list(user_id: str, specialization: str):
    doctors = doctor_service.get_doctors_by_specialization(specialization)
    rows = [{"id": f"{d['id']}", "title": d['name'], "description": f"{d['specialization']} | {d['working_hours']['start']}-{d['working_hours']['end']}"} for d in doctors]
    sections = [{"title": specialization, "rows": rows}]
    whatsapp_client.send_interactive_list(user_id, "Select Doctor", f"Available {specialization}s:", "View Doctors", sections)

def send_date_list(user_id: str, doctor_id: str):
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if not doctor:
        whatsapp_client.send_message(user_id, "Error: Doctor not found")
        return

    working_days = doctor['working_days'] # List of strings e.g. ["Monday", "Tuesday"]
    today = datetime.now()
    dates = []
    days_checked = 0
    from datetime import timedelta
    
    # Logic to find next 7 working days
    while len(dates) < 7 and days_checked < 14:
        check_date = today + timedelta(days=days_checked)
        day_name = check_date.strftime("%A")
        
        # Check partial match if needed or exact
        if day_name in working_days:
            date_str = check_date.strftime("%Y-%m-%d")
            dates.append({"id": f"date_{date_str}", "title": check_date.strftime("%A, %d %B"), "description": "Available to book"})
        days_checked += 1
    
    if not dates:
        whatsapp_client.send_message(user_id, "No available dates found.")
        return

    sections = [{"title": "Dates", "rows": dates}]
    whatsapp_client.send_interactive_list(user_id, "Select Date", f"Booking for {doctor['name']}:", "View Dates", sections)

def send_time_slots(user_id: str, doctor_id: str, date: str):
    # Get booked slots
    booked = appointment_manager.get_slots_for_doctor(doctor_id, date)
    
    # Get available
    slots = doctor_service.get_available_slots(doctor_id, date, booked)
    
    # Google Calendar Check (if enabled)
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if doctor and google_calendar_service.service and doctor.get('google_calendar_id'):
        slots = [
            s for s in slots 
            if google_calendar_service.is_slot_available(doctor['google_calendar_id'], date, s, doctor['slot_duration_minutes'])
        ]
        
    if not slots:
        # UX Improvement: Offer to choose a different date
        buttons = [
            {"id": f"dr_{doctor_id}", "title": "Choose Different Date"} # Re-triggers date selection for this doctor
        ]
        whatsapp_client.send_interactive_buttons(user_id, f"⚠️ No available slots on {date}.", buttons)
        return
    
    # Format for WhatsApp (Max 10 per list message)
    rows = [{"id": f"time_{s}", "title": datetime.strptime(s, "%H:%M").strftime("%I:%M %p")} for s in slots[:10]]
    sections = [{"title": "Available Times", "rows": rows}]
    whatsapp_client.send_interactive_list(user_id, "Select Time", f"Available on {date}:", "View Times", sections)
