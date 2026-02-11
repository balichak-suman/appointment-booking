from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional
import pytz

# Path to your service account credentials JSON file
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'credentials.json')

class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.timezone = pytz.timezone('Asia/Kolkata')  # Change to your timezone
        self.initialize_service()
    
    def initialize_service(self):
        """Initialize Google Calendar API service"""
        try:
            credentials = None
            
            # Try to load from environment variable first (for cloud deployment)
            google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
            if google_creds_json:
                import json
                creds_dict = json.loads(google_creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
                print("Google Calendar credentials loaded from environment variable")
            
            # Fall back to credentials.json file (for local development)
            elif os.path.exists(CREDENTIALS_FILE):
                credentials = service_account.Credentials.from_service_account_file(
                    CREDENTIALS_FILE,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
                print("Google Calendar credentials loaded from file")
            
            else:
                print(f"WARNING: {CREDENTIALS_FILE} not found. Google Calendar integration disabled.")
                print("To enable Google Calendar:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project and enable Google Calendar API")
                print("3. Create a service account")
                print("4. Download credentials.json and place it in the project root")
                print("   OR set GOOGLE_CREDENTIALS environment variable with the JSON content")
                return
            
            self.service = build('calendar', 'v3', credentials=credentials)
            print("Google Calendar service initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Google Calendar service: {e}")
            self.service = None
    
    def get_busy_times(self, calendar_id: str, date: str) -> List[Dict]:
        """Get busy time slots for a calendar on a specific date"""
        if not self.service:
            return []
        
        try:
            # Parse date and create time range for the day
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            time_min = self.timezone.localize(datetime.combine(date_obj, datetime.min.time()))
            time_max = time_min + timedelta(days=1)
            
            # Query freebusy
            body = {
                "timeMin": time_min.isoformat(),
                "timeMax": time_max.isoformat(),
                "items": [{"id": calendar_id}]
            }
            
            freebusy_result = self.service.freebusy().query(body=body).execute()
            
            busy_times = []
            calendar_busy = freebusy_result.get('calendars', {}).get(calendar_id, {}).get('busy', [])
            
            for busy_period in calendar_busy:
                start = datetime.fromisoformat(busy_period['start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(busy_period['end'].replace('Z', '+00:00'))
                
                # Convert to local timezone
                start_local = start.astimezone(self.timezone)
                end_local = end.astimezone(self.timezone)
                
                busy_times.append({
                    'start': start_local.strftime("%H:%M"),
                    'end': end_local.strftime("%H:%M")
                })
            
            return busy_times
            
        except Exception as e:
            print(f"Error getting busy times: {e}")
            return []
    
    def is_slot_available(self, calendar_id: str, date: str, time: str, duration_minutes: int = 30) -> bool:
        """Check if a specific time slot is available"""
        if not self.service:
            # If calendar service not available, assume slot is available
            return True
        
        try:
            # Create datetime for the slot
            date_obj = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            slot_start = self.timezone.localize(date_obj)
            slot_end = slot_start + timedelta(minutes=duration_minutes)
            
            # Get busy times
            busy_times = self.get_busy_times(calendar_id, date)
            
            # Check if slot overlaps with any busy period
            for busy in busy_times:
                busy_start = datetime.strptime(f"{date} {busy['start']}", "%Y-%m-%d %H:%M")
                busy_end = datetime.strptime(f"{date} {busy['end']}", "%Y-%m-%d %H:%M")
                busy_start = self.timezone.localize(busy_start)
                busy_end = self.timezone.localize(busy_end)
                
                # Check for overlap
                if slot_start < busy_end and slot_end > busy_start:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error checking slot availability: {e}")
            return True  # Default to available if error
    
    def create_appointment(self, calendar_id: str, patient_name: str, patient_phone: str,
                          doctor_name: str, date: str, time: str, duration_minutes: int = 30) -> Optional[str]:
        """Create a calendar event for an appointment"""
        if not self.service:
            print("Calendar service not available. Appointment not added to calendar.")
            return None
        
        try:
            # Create datetime for the appointment
            date_obj = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            start_time = self.timezone.localize(date_obj)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': f"Appointment: {patient_name}",
                'description': f"Patient: {patient_name}\nPhone: {patient_phone}\nDoctor: {doctor_name}",
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': str(self.timezone),
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': str(self.timezone),
                },
                'attendees': [
                    # Add patient email if available
                    # {'email': patient_email}
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            
            print(f"Calendar event created: {created_event.get('htmlLink')}")
            return created_event.get('id')
            
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return None
    
    def create_event(self, calendar_id: str, summary: str, description: str, start_time: str, end_time: str, date: str) -> dict:
        """Create a calendar event"""
        if not self.service:
            print("Google Calendar service not initialized")
            return None
        
        try:
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': f'{date}T{start_time}:00',
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': f'{date}T{end_time}:00',
                    'timeZone': 'Asia/Kolkata',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {created_event.get('htmlLink')}")
            return created_event
            
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
    
    def delete_event(self, calendar_id: str, date: str, start_time: str) -> bool:
        """Delete a calendar event by finding it with date and time"""
        if not self.service:
            print("Google Calendar service not initialized")
            return False
        
        try:
            # Find the event by searching for events on that date
            time_min = f'{date}T00:00:00Z'
            time_max = f'{date}T23:59:59Z'
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Find event matching the start time
            for event in events:
                event_start = event['start'].get('dateTime', event['start'].get('date'))
                if start_time in event_start:
                    # Delete the event
                    self.service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
                    print(f"Event deleted: {event.get('summary')} at {start_time}")
                    return True
            
            print(f"No event found at {date} {start_time}")
            return False
            
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

# Singleton instance
google_calendar_service = GoogleCalendarService()
