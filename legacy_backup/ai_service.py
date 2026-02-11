from groq import Groq
from config import config
from typing import Dict, Any
from datetime import datetime
from dateutil import parser as date_parser
import re

groq_client = None
if config.GROQ_API_KEY:
    groq_client = Groq(api_key=config.GROQ_API_KEY)

class AIService:
    @staticmethod
    def parse_natural_date(text: str) -> str:
        """Parse natural language date to YYYY-MM-DD format"""
        try:
            # Common patterns
            text_lower = text.lower().strip()
            today = datetime.now()
            
            # Handle relative dates
            if text_lower in ['today', 'now']:
                return today.strftime("%Y-%m-%d")
            elif text_lower == 'tomorrow':
                return (today + timedelta(days=1)).strftime("%Y-%m-%d")
            elif text_lower == 'day after tomorrow':
                return (today + timedelta(days=2)).strftime("%Y-%m-%d")
            elif 'next week' in text_lower:
                return (today + timedelta(days=7)).strftime("%Y-%m-%d")
            
            # Try to parse with dateutil (handles "12th Feb", "February 12", etc.)
            parsed_date = date_parser.parse(text, fuzzy=True, default=today)
            
            # If parsed date is in the past, assume next year
            if parsed_date.date() < today.date():
                parsed_date = parsed_date.replace(year=today.year + 1)
            
            return parsed_date.strftime("%Y-%m-%d")
            
        except Exception as e:
            print(f"Error parsing date '{text}': {e}")
            return None
    
    @staticmethod
    def parse_natural_time(text: str) -> str:
        """Parse natural language time to HH:MM format"""
        try:
            text_lower = text.lower().strip()
            
            # Handle common time expressions
            time_mappings = {
                'morning': '09:00',
                'afternoon': '14:00',
                'evening': '17:00',
                'noon': '12:00',
                'midnight': '00:00'
            }
            
            if text_lower in time_mappings:
                return time_mappings[text_lower]
            
            # Handle "3 PM", "3PM", "15:00", etc.
            # Try to parse with dateutil
            parsed_time = date_parser.parse(text, fuzzy=True)
            return parsed_time.strftime("%H:%M")
            
        except Exception as e:
            print(f"Error parsing time '{text}': {e}")
            return None
    
    @staticmethod
    def parse_intent(message: str) -> Dict[str, Any]:
        """Parse user intent using Groq AI with enhanced date/time parsing"""
        if not groq_client:
            print("Groq SDK not initialized. Returning default intent.")
            return {"intent": "other", "entities": {}, "response": "I can help you book an appointment. Just say 'Book appointment'."}
        
        try:
            completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an assistant for a hospital appointment booking bot. 
Analyze the user's message and extract the intent and entities.
Current Date: {datetime.now().strftime("%Y-%m-%d")}
Current Day: {datetime.now().strftime("%A")}

Intents:
- book_appointment: User wants to book an appointment
- cancel_appointment: User wants to cancel
- check_availability: User wants to check available slots
- select_doctor: User is selecting a doctor
- select_specialization: User is selecting a specialization
- other: Greetings or unrelated queries

IMPORTANT: For dates, extract the EXACT text the user mentioned (e.g., "12th Feb", "tomorrow", "next Monday").
For times, extract the EXACT text (e.g., "3 PM", "afternoon", "morning").
Do NOT convert them to standard format - just extract what the user said.

Return ONLY valid JSON in the following format:
{{{{
  "intent": "string",
  "entities": {{{{
    "date_text": "exact date text user mentioned (if any)",
    "time_text": "exact time text user mentioned (if any)",
    "specialization": "string (if mentioned)",
    "doctor_name": "string (if mentioned)",
    "doctor_number": "number if user selected by number (if mentioned)"
  }}}},
  "response": "A polite, short response"
}}}}"""
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            content = completion.choices[0].message.content
            if not content:
                raise Exception("No content from AI")
            
            import json
            result = json.loads(content)
            
            # Parse natural language dates and times
            entities = result.get("entities", {})
            
            if entities.get("date_text"):
                parsed_date = AIService.parse_natural_date(entities["date_text"])
                if parsed_date:
                    entities["date"] = parsed_date
                    entities["original_date_text"] = entities["date_text"]
            
            if entities.get("time_text"):
                parsed_time = AIService.parse_natural_time(entities["time_text"])
                if parsed_time:
                    entities["time"] = parsed_time
                    entities["original_time_text"] = entities["time_text"]
            
            result["entities"] = entities
            return result
            
        except Exception as error:
            print(f"Error parsing intent: {error}")
            return {"intent": "other", "entities": {}, "response": "I can help you book an appointment. Just say 'Book appointment'."}

# Import timedelta for date calculations
from datetime import timedelta

ai_service = AIService()
