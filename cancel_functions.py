# Add these functions at the end of app.py before if __name__ == "__main__":

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
