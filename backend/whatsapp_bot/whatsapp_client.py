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
    
    def _format_phone_number(self, phone: str) -> str:
        """Helper to format phone number to E.164 without +"""
        clean_phone = ''.join(filter(str.isdigit, phone))
        # Assuming India (91) if length is 10
        if len(clean_phone) == 10:
            return f"91{clean_phone}"
        # If it starts with 0, remove it and add 91
        if clean_phone.startswith('0') and len(clean_phone) == 11:
             return f"91{clean_phone[1:]}"
        return clean_phone

    def send_message(self, to: str, message: str):
        """Send a simple text message"""
        formatted_to = self._format_phone_number(to)
        payload = {
            "messaging_product": "whatsapp",
            "to": formatted_to,
            "type": "text",
            "text": {"body": message}
        }
        
        print(f"Sending WhatsApp message to {formatted_to}: {message}")
        
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
        
        formatted_to = self._format_phone_number(to)
        payload["to"] = formatted_to
        
        print(f"Sending interactive list to {formatted_to}")
        
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
        
        formatted_to = self._format_phone_number(to)
        payload["to"] = formatted_to
        
        print(f"Sending interactive buttons to {formatted_to}")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error sending interactive buttons: {error}")
            if hasattr(error, 'response') and error.response is not None:
                print(f"Response: {error.response.text}")
    def send_template(self, to: str, template_name: str, language_code: str = "en_US", components: list = None):
        """
        Send a WhatsApp Template Message
        
        components format:
        [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "value1"},
                    {"type": "text", "text": "value2"}
                ]
            }
        ]
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }


        formatted_to = self._format_phone_number(to)
        payload["to"] = formatted_to
        
        print(f"Sending Template '{template_name}' to {formatted_to}")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error sending template: {error}")
            if hasattr(error, 'response') and error.response is not None:
                print(f"Response: {error.response.text}")
            raise

whatsapp_client = WhatsAppClient()
