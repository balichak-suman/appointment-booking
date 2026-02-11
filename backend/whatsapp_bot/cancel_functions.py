from .whatsapp_client import whatsapp_client
from .appointment_manager import appointment_manager
from .google_calendar_service import google_calendar_service
from .doctor_service import doctor_service
from datetime import datetime

# whatsapp_client, etc are already instantiated in their modules, 
# but imported names conflict with local variable names if not careful.
# The original file instantiated them. Here we import the instances.

def show_user_appointments(user_id: str):
    """Show user's upcoming appointments"""
    appointments = appointment_manager.get_user_appointments(user_id)
    
    if not appointments:
        whatsapp_client.send_message(user_id, "You don't have any appointments to cancel.")
        return
    
    # Filter upcoming appointments only
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
    for idx, apt in enumerate(upcoming):
        doctor_name = apt.get('doctorName', 'Unknown Doctor')
        date = apt.get('date')
        time = apt.get('time')
        
        # Format date nicely
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d %B %Y")
        except:
            formatted_date = date
        
        # Convert time to 12h format
        try:
            time_obj = datetime.strptime(time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")
        except:
            formatted_time = time
        
        # Use appointment ID directly
        apt_id = apt.get('id')
        
        # Pass ID directly. No need for index unless we have duplicate IDs which shouldn't happen in DB.
        # But to be safe and match original logic pattern:
        rows.append({
            "id": f"cancel_{apt_id}",
            "title": f"{doctor_name}",
            "description": f"{formatted_date} at {formatted_time}"
        })
    
    sections = [{"title": "Your Appointments", "rows": rows}]
    
    whatsapp_client.send_interactive_list(
        user_id,
        "Cancel Appointment",
        "Select an appointment to cancel:",
        "View Appointments",
        sections
    )

def cancel_appointment(user_id: str, appointment_id: str):
    """Cancel a specific appointment"""
    # The appointment_id comes as "cancel_apt_id" or "cancel_apt_id_index" from interactive list
    # logic in api/whatsapp.py splits by "_" and sends the second part as appointment_id
    
    actual_apt_id = appointment_id
    if "_" in appointment_id:
        # If passed full string "cancel_123", we might need to parse. 
        # But api/whatsapp.py does: parts = interaction_id.split("_"); if len>=2: apt_id = parts[1]
        # So we expect actual_apt_id to be just "123".
        pass 
        
    # Get appointment details
    appointments = appointment_manager.get_user_appointments(user_id)
    appointment = None
    
    for apt in appointments:
        if str(apt.get('id')) == str(actual_apt_id):
            appointment = apt
            break
    
    if not appointment:
        whatsapp_client.send_message(user_id, "Appointment not found.")
        return
    
    # Get appointment details for deletion
    doctor_id = appointment.get('doctorId')
    date = appointment.get('date')
    time = appointment.get('time')
    doctor_name = appointment.get('doctorName', 'Unknown Doctor')
    
    # Delete from Google Calendar
    if doctor_id:
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if doctor and google_calendar_service.service:
            calendar_id = doctor.get('google_calendar_id')
            # working_days etc are in doctor dict
            # We don't have event_id stored in DB yet (Task for later improvement).
            # The original google_calendar_service.delete_event uses calendar_id, date, and time to find event.
            if calendar_id:
                google_calendar_service.delete_event(calendar_id, date, time)
    
    # Delete from DB
    success = appointment_manager.cancel_appointment(actual_apt_id)
    
    if success:
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
