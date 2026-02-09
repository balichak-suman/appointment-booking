import requests
from config import config
from typing import List, Optional, Dict, Any

class AisensyClient:
    @staticmethod
    def send_message(destination: str, user_name: str, template_params: List[str] = None) -> Optional[Dict[str, Any]]:
        """Send a template message via Aisensy"""
        if template_params is None:
            template_params = []
            
        try:
            if not config.AISENSY_API_KEY or not config.AISENSY_CAMPAIGN_NAME:
                print("⚠️  Aisensy logic skipped (Missing Key/Campaign). MOCK SENDING:")
                print(f"To: {destination}")
                print(f"Msg: {template_params}")
                return {"success": True, "mock": True}
            
            payload = {
                "apiKey": config.AISENSY_API_KEY,
                "campaignName": config.AISENSY_CAMPAIGN_NAME,
                "destination": destination,
                "userName": user_name,
                "templateParams": template_params
            }
            
            print(f"Sending Aisensy message: {payload}")
            
            response = requests.post(
                config.AISENSY_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Aisensy response: {response.json()}")
            return response.json()
            
        except Exception as error:
            print(f"Error sending Aisensy message: {error}")
            return None

aisensy_client = AisensyClient()
