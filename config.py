import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.getenv('PORT', 8000))
    
    # WhatsApp Business API Configuration
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
    WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'my_verify_token_123')
    WHATSAPP_API_URL = 'https://graph.facebook.com/v21.0'
    
    # Groq Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

config = Config()
