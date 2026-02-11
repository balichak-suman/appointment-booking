import requests
from .config import config
import json

class WhatsAppClient:
    def __init__(self):
        self.api_url = f"{config.WHATSAPP_API_URL}/{config.WHATSAPP_PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {config.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, to: str, message: str):
        """Send a simple text message"""
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        print(f"Sending WhatsApp message to {to}: {message}")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error sending WhatsApp message: {error}")
            if hasattr(error, 'response') and error.response is not None:
                print(f"Response: {error.response.text}")
            raise
    
    def send_interactive_list(self, to: str, header: str, body: str, button_text: str, sections: list):
        """
        Send an interactive list message
        
        sections format:
        [
            {
                "title": "Section Title",
                "rows": [
                    {"id": "unique_id", "title": "Row Title", "description": "Optional description"}
                ]
            }
        ]
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": header},
                "body": {"text": body},
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }
        
        print(f"Sending interactive list to {to}")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error sending interactive list: {error}")
            if hasattr(error, 'response') and error.response is not None:
                print(f"Response: {error.response.text}")
            raise
    
    def send_interactive_buttons(self, to: str, body: str, buttons: list):
        """
        Send interactive reply buttons (max 3 buttons)
        
        buttons format:
        [
            {"id": "unique_id", "title": "Button Text"}
        ]
        """
        if len(buttons) > 3:
            buttons = buttons[:3]  # WhatsApp allows max 3 buttons
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": btn} for btn in buttons
                    ]
                }
            }
        }
        
        print(f"Sending interactive buttons to {to}")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error sending interactive buttons: {error}")
            if hasattr(error, 'response') and error.response is not None:
                print(f"Response: {error.response.text}")
            raise

whatsapp_client = WhatsAppClient()
