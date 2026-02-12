from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

CREDENTIALS_FILE = 'credentials.json'

def debug_calendar():
    try:
        # Load credentials
        if os.path.exists(CREDENTIALS_FILE):
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/calendar']
            )
            
            # Print WHO we are logged in as
            with open(CREDENTIALS_FILE) as f:
                data = json.load(f)
                email = data.get('client_email')
                print(f"\n[DEBUG] I am logged in as the Service Account:")
                print(f"   Email: {email}")
                print(f"   (This is NOT your personal email!)\n")

            service = build('calendar', 'v3', credentials=creds)

            # unexpected, but let's try listing calendars
            print("[DEBUG] Calendars accessible to this Service Account:")
            calendar_list = service.calendarList().list().execute()
            found_user_email = False
            
            for calendar_list_entry in calendar_list['items']:
                cal_id = calendar_list_entry['id']
                print(f"   - {calendar_list_entry['summary']} (ID: {cal_id})")
                
            print("\n[CONCLUSION]")
            print(f"I can ONLY write to the calendars listed above.")
            print(f"To write to YOUR personal calendar, you must SHARE it with: {email}")
            
        else:
            print(f"File {CREDENTIALS_FILE} not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_calendar()
