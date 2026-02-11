from .whatsapp_client import whatsapp_client
from .appointment_manager import appointment_manager
from .google_calendar_service import google_calendar_service
from .doctor_service import doctor_service

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
    
    # Create list of appointments with unique IDs
    rows = []
    for idx, apt in enumerate(upcoming):
        # Use camelCase keys to match appointment data structure
        doctor_name = apt.get('doctorName', 'Unknown Doctor')
        date = apt.get('date')
        time = apt.get('time')
        
        # Format date nicely
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        
        # Convert time to 12h format
        time_obj = datetime.strptime(time, "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")
        
        # Use appointment ID directly with index to ensure uniqueness
        apt_id = apt.get('id')
        
        rows.append({
            "id": f"cancel_{apt_id}_{idx}",
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
    # The appointment_id comes as "cancel_apt_id_index"
    # Remove the index (last part after splitting by _)
    parts = appointment_id.split("_")
    
    if len(parts) < 2:
        whatsapp_client.send_message(user_id, "Error: Invalid appointment ID")
        return
    
    # Remove the index (last part) to get the actual appointment ID
    actual_apt_id = "_".join(parts[:-1])
    
    # Get appointment details
    appointments = appointment_manager.get_user_appointments(user_id)
    appointment = None
    
    # Use camelCase keys to match appointment data structure
    for apt in appointments:
        if apt.get('id') == actual_apt_id:
            appointment = apt
            break
    
    if not appointment:
        whatsapp_client.send_message(user_id, "Appointment not found.")
        return
    
    # Get appointment details for deletion
    doctor_id = appointment.get('doctorId')
    date = appointment.get('date')
    time = appointment.get('time')
    
    # Delete from Google Calendar
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if doctor and google_calendar_service.service:
        calendar_id = doctor.get('google_calendar_id')
        if calendar_id:
            google_calendar_service.delete_event(calendar_id, date, time)
    
    # Cancel in the database using appointment ID
    success = appointment_manager.cancel_appointment(actual_apt_id)
    
    if success:
        doctor_name = appointment.get('doctorName', 'Unknown Doctor')
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
