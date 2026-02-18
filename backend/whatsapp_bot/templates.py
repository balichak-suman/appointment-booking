class WhatsAppTemplates:
    APPOINTMENT_CONFIRMATION = "appointment_confirmation"
    APPOINTMENT_REMINDER = "appointment_reminder"

    @staticmethod
    def get_confirmation_components(patient_name, doctor_name, date, time):
        return [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": patient_name},
                    {"type": "text", "text": doctor_name},
                    {"type": "text", "text": str(date)},
                    {"type": "text", "text": time}
                ]
            }
        ]

    @staticmethod
    def get_reminder_components(patient_name, doctor_name, time):
        return [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": patient_name},
                    {"type": "text", "text": doctor_name},
                    {"type": "text", "text": time}
                ]
            }
        ]
