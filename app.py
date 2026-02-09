from flask import Flask, request, jsonify, send_from_directory
from config import config
from whatsapp_client import whatsapp_client
from appointment_manager import appointment_manager
from doctor_service import doctor_service
from google_calendar_service import google_calendar_service
from datetime import datetime, timedelta

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server_debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

@app.before_request
def log_request_info():
    logger.debug(f"Incoming Request: {request.method} {request.path}")
    if request.is_json:
        logger.debug(f"JSON Body: {request.get_json()}")

@app.route('/test')
def test_route():
    return "Test route works!", 200

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/webhook', methods=['GET', 'POST'], strict_slashes=False)
def webhook():
    """Webhook endpoint for receiving messages and verification"""
    
    # Handle Webhook Verification (GET)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == config.WHATSAPP_VERIFY_TOKEN:
                print("Webhook verified successfully!")
                return challenge, 200
            else:
                return jsonify({"status": "error", "message": "Verification failed"}), 403
    
    # Handle Incoming Messages (POST)
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        
        if data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    
                    # Handle interactive message responses
                    if 'messages' in value:
                        for message in value['messages']:
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
                                handle_incoming_message(sender, sender_name, message_body, None)
                            
                            elif message_type == 'interactive':
                                interactive = message.get('interactive', {})
                                interactive_type = interactive.get('type')
                                
                                if interactive_type == 'list_reply':
                                    # User selected from list
                                    list_reply = interactive.get('list_reply', {})
                                    selection_id = list_reply.get('id')
                                    handle_incoming_message(sender, sender_name, '', selection_id)
                                
                                elif interactive_type == 'button_reply':
                                    # User clicked a button
                                    button_reply = interactive.get('button_reply', {})
                                    button_id = button_reply.get('id')
                                    handle_incoming_message(sender, sender_name, '', button_id)
                                
        return jsonify({"status": "EVENT_RECEIVED"}), 200
        
    except Exception as error:
        logger.error(f"Error processing webhook: {error}")
        return jsonify({"status": "Error", "message": str(error)}), 500

def handle_incoming_message(user_id: str, user_name: str, text: str, button_id: str):
    """Handle incoming message or button click"""
    session = appointment_manager.get_session(user_id)
    
    # If user sent text and not in a flow, check for booking intent
    if text and session["step"] == "idle":
        text_lower = text.lower()
        if any(word in text_lower for word in ['book', 'appointment', 'doctor', 'schedule']):
            # Start booking flow
            appointment_manager.update_session(user_id, {
                "step": "awaiting_specialization",
                "tempData": {"userName": user_name}
            })
            send_specialization_list(user_id)
        else:
            # Welcome message with Book, Cancel, and Reschedule options as buttons
            whatsapp_client.send_interactive_buttons(
                user_id,
                "Welcome to Hospital Appointment Booking!\n\nWhat would you like to do?",
                [
                    {"id": "book_appointment", "title": "📅 Book Appointment"},
                    {"id": "cancel_appointment", "title": "❌ Cancel"},
                    {"id": "reschedule_appointment", "title": "🔄 Reschedule"}
                ]
            )
        return
    
    # Handle button/list selections
    if button_id:
        handle_button_selection(user_id, user_name, button_id, session)

def send_specialization_list(user_id: str):
    """Send interactive list of specializations"""
    specializations = doctor_service.get_specializations()
    
    rows = []
    for spec in specializations:
        # Count doctors in this specialization
        doctors = doctor_service.get_doctors_by_specialization(spec)
        count = len(doctors)
        rows.append({
            "id": f"spec_{spec}",
            "title": spec,
            "description": f"{count} doctor{'s' if count > 1 else ''} available"
        })
    
    sections = [{"title": "Specializations", "rows": rows}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Choose Specialization",
        "What type of doctor do you need?",
        "View Specializations",
        sections
    )

def send_doctor_list(user_id: str, specialization: str = None):
    """Send interactive list of doctors, optionally filtered by specialization"""
    if specialization:
        doctors = doctor_service.get_doctors_by_specialization(specialization)
    else:
        doctors = doctor_service.get_all_doctors()
    
    rows = []
    for doctor in doctors:
        # Show working hours instead of days since they work every day
        hours = f"{doctor['working_hours']['start']}-{doctor['working_hours']['end']}"
        rows.append({
            "id": doctor['id'],
            "title": doctor['name'],
            "description": f"{doctor['specialization']} | Every day | {hours}"
        })
    
    title = specialization if specialization else "Doctors"
    sections = [{"title": title, "rows": rows}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Select a Doctor",
        "Choose from our available doctors:",
        "View Doctors",
        sections
    )

def send_date_buttons(user_id: str, doctor_id: str):
    """Send date selection as a list message - shows all 7 dates in one message"""
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if not doctor:
        whatsapp_client.send_message(user_id, "Error: Doctor not found")
        return
    
    working_days = doctor['working_days']
    today = datetime.now()
    dates = []
    
    # Find next 7 working days for this doctor
    days_checked = 0
    while len(dates) < 7 and days_checked < 14:  # Check up to 2 weeks ahead
        check_date = today + timedelta(days=days_checked)
        day_name = check_date.strftime("%A")
        
        if day_name in working_days:
            date_str = check_date.strftime("%Y-%m-%d")
            
            if days_checked == 0:
                label = f"Today ({day_name})"
                description = check_date.strftime("%d %B %Y")
            elif days_checked == 1:
                label = f"Tomorrow ({day_name})"
                description = check_date.strftime("%d %B %Y")
            else:
                label = f"{day_name}"
                description = check_date.strftime("%d %B %Y")
            
            dates.append({
                "id": f"date_{date_str}",
                "title": label,
                "description": description
            })
        
        days_checked += 1
    
    if not dates:
        whatsapp_client.send_message(user_id, f"Sorry, {doctor['name']} has no available dates in the next 2 weeks.")
        return
    
    # Send as list message (can show up to 10 items in one message)
    sections = [{"title": "Dates", "rows": dates}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Select Date",
        f"Choose a date for {doctor['name']}:",
        "View Dates",
        sections
    )

def send_time_slots(user_id: str, doctor_id: str, date: str):
    """Send available time slot list - shows all slots in one message"""
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    calendar_id = doctor.get('google_calendar_id')
    
    # Get booked appointments from local storage
    booked = appointment_manager.get_doctor_appointments(doctor_id, date)
    
    # Get available slots
    available_slots = doctor_service.get_available_slots(doctor_id, date, booked)
    
    # Filter by Google Calendar availability if enabled
    if google_calendar_service.service and calendar_id:
        available_slots = [
            slot for slot in available_slots
            if google_calendar_service.is_slot_available(calendar_id, date, slot, doctor['slot_duration_minutes'])
        ]
    
    # Filter out past time slots if booking for today
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    if date == today:
        current_time = datetime.now().strftime("%H:%M")
        available_slots = [slot for slot in available_slots if slot > current_time]
    
    if not available_slots:
        whatsapp_client.send_message(user_id, "Sorry, no available slots on this date. Please select another date.")
        send_date_buttons(user_id, doctor_id)
        return
    
    # Convert slots to list format
    rows = []
    for slot in available_slots:
        # Convert 24h to 12h format for better readability
        time_obj = datetime.strptime(slot, "%H:%M")
        time_12h = time_obj.strftime("%I:%M %p")
        
        rows.append({
            "id": f"time_{slot}",
            "title": time_12h,
            "description": f"Duration: {doctor['slot_duration_minutes']} minutes"
        })
    
    # Send as list message (can show up to 10 items per section)
    # WhatsApp has a hard limit of 10 rows total per message
    # Send multiple messages if needed
    total_slots = len(rows)
    
    if total_slots <= 10:
        # All slots fit in one message
        sections = [{"title": f"{total_slots} Slots", "rows": rows}]
        whatsapp_client.send_interactive_list(
            user_id,
            "Select Time",
            f"Available slots for {doctor['name']} on {date}:",
            "View Times",
            sections
        )
    else:
        # Need multiple messages
        # First message: slots 1-10
        sections = [{"title": f"Slots 1-10 of {total_slots}", "rows": rows[:10]}]
        whatsapp_client.send_interactive_list(
            user_id,
            "Select Time",
            f"Available slots for {doctor['name']} on {date}:",
            "View Times (1-10)",
            sections
        )
        
        # Second message: remaining slots (11+)
        remaining = rows[10:]
        if len(remaining) <= 10:
            sections = [{"title": f"Slots 11-{total_slots}", "rows": remaining}]
            whatsapp_client.send_interactive_list(
                user_id,
                "More Times",
                f"More available slots:",
                "View Times (11+)",
                sections
            )
        else:
            # If still more than 10, send third message
            sections = [{"title": f"Slots 11-20", "rows": remaining[:10]}]
            whatsapp_client.send_interactive_list(
                user_id,
                "More Times",
                f"More available slots:",
                "View Times (11-20)",
                sections
            )
            
            if len(remaining) > 10:
                sections = [{"title": f"Slots 21-{total_slots}", "rows": remaining[10:]}]
                whatsapp_client.send_interactive_list(
                    user_id,
                    "More Times",
                    f"Even more slots:",
                    "View Times (21+)",
                    sections
                )

def handle_button_selection(user_id: str, user_name: str, button_id: str, session: dict):
    """Handle button/list selection"""
    step = session.get("step")
    
    # Book appointment button
    if button_id == "book_appointment":
        send_specialization_list(user_id)
        appointment_manager.update_session(user_id, {
            "step": "awaiting_specialization",
            "tempData": {"userName": user_name}
        })
        return
    
    # Cancel appointment button
    if button_id == "cancel_appointment":
        show_user_appointments(user_id)
        return
    
    # Cancel specific appointment
    if button_id.startswith("cancel_"):
        appointment_id = button_id.replace("cancel_", "")
        cancel_appointment(user_id, appointment_id)
        return
    
    # Reschedule appointment button
    if button_id == "reschedule_appointment":
        show_appointments_for_reschedule(user_id)
        return
    
    # Reschedule specific appointment
    if button_id.startswith("reschedule_"):
        appointment_id = button_id.replace("reschedule_", "")
        start_reschedule(user_id, appointment_id)
        return
    
    # Specialization selection
    if button_id.startswith("spec_"):
        specialization = button_id.replace("spec_", "")
        appointment_manager.update_session(user_id, {
            "step": "awaiting_doctor",
            "tempData": {
                **session["tempData"],
                "specialization": specialization
            }
        })
        send_doctor_list(user_id, specialization)
        return
    
    # Doctor selection
    if button_id.startswith("dr_"):
        doctor = doctor_service.get_doctor_by_id(button_id)
        if doctor:
            appointment_manager.update_session(user_id, {
                "step": "awaiting_date",
                "tempData": {
                    **session["tempData"],
                    "doctor_id": doctor['id'],
                    "doctor_name": doctor['name'],
                    "specialization": doctor['specialization']
                }
            })
            send_date_buttons(user_id, doctor['id'])
        return
    
    # Date selection
    if button_id.startswith("date_"):
        date = button_id.replace("date_", "")
        doctor_id = session["tempData"].get("doctor_id")
        step = session.get("step")
        
        # Check if this is a reschedule or new booking
        if step == "awaiting_reschedule_date":
            # Rescheduling flow
            appointment_manager.update_session(user_id, {
                "step": "awaiting_reschedule_time",
                "tempData": {
                    **session["tempData"],
                    "new_date": date
                }
            })
        else:
            # Normal booking flow
            appointment_manager.update_session(user_id, {
                "step": "awaiting_time",
                "tempData": {
                    **session["tempData"],
                    "date": date
                }
            })
        
        send_time_slots(user_id, doctor_id, date)
    # Time selection
    if button_id.startswith("time_"):
        time = button_id.replace("time_", "")
        step = session.get("step")
        
        try:
            # Get session data
            doctor_id = session["tempData"].get("doctor_id")
            doctor_name = session["tempData"].get("doctor_name")
            specialization = session["tempData"].get("specialization")
            user_name = session["tempData"].get("userName")
            
            # Check if this is a reschedule or new booking
            if step == "awaiting_reschedule_time":
                # Rescheduling flow - cancel old and create new
                old_date = session["tempData"].get("old_date")
                old_time = session["tempData"].get("old_time")
                new_date = session["tempData"].get("new_date")
                appointment_id = session["tempData"].get("appointment_id")
                
                # Delete old appointment from Google Calendar
                doctor = doctor_service.get_doctor_by_id(doctor_id)
                if doctor and google_calendar_service.service:
                    calendar_id = doctor.get('google_calendar_id')
                    if calendar_id:
                        google_calendar_service.delete_event(calendar_id, old_date, old_time)
                
                # Cancel old appointment in local storage using appointment ID
                appointment_manager.cancel_appointment(appointment_id)
                
                # Create new appointment
                appointment = appointment_manager.create_appointment(
                    user_id,
                    user_name,
                    doctor_id,
                    doctor_name,
                    specialization,
                    new_date,
                    time
                )
                
                # Create new Google Calendar event
                if google_calendar_service.service and calendar_id:
                    google_calendar_service.create_appointment(
                        calendar_id,
                        user_name,
                        user_id,
                        doctor_name,
                        new_date,
                        time,
                        doctor['slot_duration_minutes']
                    )
                
                # Clear session
                appointment_manager.clear_session(user_id)
                
                # Send confirmation
                whatsapp_client.send_message(
                    user_id,
                    f"✅ Appointment rescheduled successfully!\n\n"
                    f"Doctor: {doctor_name}\n"
                    f"Old: {old_date} at {old_time}\n"
                    f"New: {new_date} at {time}\n\n"
                    f"See you then!"
                )
                return
            
            else:
                # Normal booking flow
                date = session["tempData"].get("date")
                
                # Create appointment
                appointment = appointment_manager.create_appointment(
                    user_id,
                    user_name,
                    doctor_id,
                    doctor_name,
                    specialization,
                    date,
                    time
                )
                
                # Create Google Calendar event
                doctor = doctor_service.get_doctor_by_id(doctor_id)
                calendar_id = doctor.get('google_calendar_id')
                
                if google_calendar_service.service and calendar_id:
                    google_calendar_service.create_appointment(
                        calendar_id,
                        user_name,
                        user_id,
                        doctor_name,
                        date,
                        time,
                        doctor['slot_duration_minutes']
                    )
                
                # Clear session
                appointment_manager.clear_session(user_id)
                
                # Send confirmation
                confirmation = f"*Appointment Confirmed!*\n\n"
                confirmation += f"ID: {appointment['id']}\n"
                confirmation += f"Doctor: {doctor_name}\n"
                confirmation += f"Specialization: {specialization}\n"
                confirmation += f"Date: {date}\n"
                confirmation += f"Time: {time}\n\n"
                confirmation += "See you then!"
                
                whatsapp_client.send_message(user_id, confirmation)
                return
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error creating appointment: {e}")
            print(f"Full traceback: {error_details}")
            whatsapp_client.send_message(user_id, f"Sorry, there was an error creating your appointment.\n\nError: {str(e)}\n\nPlease try again.")

def show_user_appointments(user_id: str):
    """Show user's upcoming appointments"""
    appointments = appointment_manager.get_user_appointments(user_id)
    
    if not appointments:
        whatsapp_client.send_message(user_id, "You don't have any appointments to cancel.")
        return
    
    # Filter upcoming appointments only
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    upcoming = []
    for apt in appointments:
        apt_date = apt.get('date')
        apt_time = apt.get('time')
        
        # Include if date is in future, or today but time hasn't passed
        if apt_date > today or (apt_date == today and apt_time > current_time):
            upcoming.append(apt)
    
    if not upcoming:
        whatsapp_client.send_message(user_id, "You don't have any upcoming appointments to cancel.")
        return
    
    # Create list of appointments
    rows = []
    for apt in upcoming:
        doctor_name = apt.get('doctor_name', 'Unknown Doctor')
        date = apt.get('date')
        time = apt.get('time')
        
        # Format date nicely
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        
        # Convert time to 12h format
        time_obj = datetime.strptime(time, "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")
        
        # Create unique ID for this appointment
        apt_id = f"{apt.get('doctor_id')}_{date}_{time}"
        
        rows.append({
            "id": f"cancel_{apt_id}",
            "title": f"{doctor_name}",
            "description": f"{formatted_date} at {formatted_time}"
        })
    
    sections = [{"title": "Appointments", "rows": rows}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Cancel Appointment",
        "Select an appointment to cancel:",
        "View Appointments",
        sections
    )

def cancel_appointment(user_id: str, appointment_id: str):
    """Cancel a specific appointment"""
    # Parse appointment ID
    parts = appointment_id.split("_")
    if len(parts) < 3:
        whatsapp_client.send_message(user_id, "Error: Invalid appointment ID")
        return
    
    doctor_id = parts[0]
    date = parts[1]
    time = parts[2]
    
    # Get appointment details
    appointments = appointment_manager.get_user_appointments(user_id)
    appointment = None
    
    for apt in appointments:
        if apt.get('doctor_id') == doctor_id and apt.get('date') == date and apt.get('time') == time:
            appointment = apt
            break
    
    if not appointment:
        whatsapp_client.send_message(user_id, "Appointment not found.")
        return
    
    # Delete from Google Calendar
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if doctor and google_calendar_service.service:
        calendar_id = doctor.get('google_calendar_id')
        if calendar_id:
            google_calendar_service.delete_event(calendar_id, date, time)
    
    # Delete from local storage
    success = appointment_manager.cancel_appointment(user_id, doctor_id, date, time)
    
    if success:
        doctor_name = appointment.get('doctor_name', 'Unknown Doctor')
        whatsapp_client.send_message(
            user_id,
            f"✅ Appointment cancelled successfully!\n\n"
            f"Doctor: {doctor_name}\n"
            f"Date: {date}\n"
            f"Time: {time}\n\n"
            f"You can book a new appointment anytime."
        )
    else:
        whatsapp_client.send_message(user_id, "Failed to cancel appointment. Please try again.")

def show_appointments_for_reschedule(user_id: str):
    """Show user's upcoming appointments for rescheduling"""
    appointments = appointment_manager.get_user_appointments(user_id)
    
    if not appointments:
        whatsapp_client.send_message(user_id, "You don't have any appointments to reschedule.")
        return
    
    # Filter upcoming appointments only
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    upcoming = []
    for apt in appointments:
        apt_date = apt.get('date')
        apt_time = apt.get('time')
        
        # Include if date is in future, or today but time hasn't passed
        if apt_date > today or (apt_date == today and apt_time > current_time):
            upcoming.append(apt)
    
    if not upcoming:
        whatsapp_client.send_message(user_id, "You don't have any upcoming appointments to reschedule.")
        return
    
    # Create list of appointments with unique IDs
    rows = []
    for idx, apt in enumerate(upcoming):
        # Use camelCase keys to match appointment data structure
        doctor_name = apt.get('doctorName', 'Unknown Doctor')
        date = apt.get('date')
        time = apt.get('time')
        doctor_id = apt.get('doctorId')
        
        # Format date nicely
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        
        # Convert time to 12h format
        time_obj = datetime.strptime(time, "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")
        
        # Create unique ID with index to prevent duplicates
        apt_id = f"{doctor_id}_{date}_{time}_{idx}"
        
        rows.append({
            "id": f"reschedule_{apt_id}",
            "title": f"{doctor_name}",
            "description": f"{formatted_date} at {formatted_time}"
        })
    
    sections = [{"title": "Appointments", "rows": rows}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Reschedule Appointment",
        "Select appointment to reschedule:",
        "View Appointments",
        sections
    )

def start_reschedule(user_id: str, appointment_id: str):
    """Start the rescheduling process"""
    # Parse appointment ID (format: doctor_id_date_time_index)
    # Example: dr_001_2026-02-09_16:30_3
    parts = appointment_id.split("_")
    
    # Reconstruct properly: dr_001, 2026-02-09, 16:30, 3
    if len(parts) < 5:
        whatsapp_client.send_message(user_id, "Error: Invalid appointment ID format")
        return
    
    # doctor_id is parts[0]_parts[1] (e.g., "dr_001")
    doctor_id = f"{parts[0]}_{parts[1]}"
    # date is parts[2] (e.g., "2026-02-09")
    old_date = parts[2]
    # time is parts[3] (e.g., "16:30")
    old_time = parts[3]
    # index is parts[4] (we don't need it)
    
    # Get appointment details
    appointments = appointment_manager.get_user_appointments(user_id)
    appointment = None
    
    # Use camelCase keys to match appointment data structure
    for apt in appointments:
        if apt.get('doctorId') == doctor_id and apt.get('date') == old_date and apt.get('time') == old_time:
            appointment = apt
            break
    
    if not appointment:
        whatsapp_client.send_message(user_id, f"Appointment not found.\nLooking for: Doctor={doctor_id}, Date={old_date}, Time={old_time}")
        return
    
    # Store old appointment info in session for rescheduling
    appointment_manager.update_session(user_id, {
        "step": "awaiting_reschedule_date",
        "tempData": {
            "userName": appointment.get('userName'),
            "doctor_id": doctor_id,
            "doctor_name": appointment.get('doctorName'),
            "specialization": appointment.get('specialization'),
            "old_date": old_date,
            "old_time": old_time,
            "appointment_id": appointment.get('id')
        }
    })
    
    # Show date selection for new appointment
    send_date_buttons(user_id, doctor_id)

if __name__ == '__main__':
    print(f"Server running on port {config.PORT}")
    print(f"Loaded {len(doctor_service.get_all_doctors())} doctors")
    print(f"Google Calendar: {'Enabled' if google_calendar_service.service else 'Disabled (credentials.json not found)'}")
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
