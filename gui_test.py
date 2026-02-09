import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import re
from ai_service import ai_service
from appointment_manager import appointment_manager
from whatsapp_client import whatsapp_client

class WhatsAppBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Hospital Appointment Bot Tester")
        self.root.geometry("600x800")
        self.root.configure(bg="#f0f0f0")
        
        # User info
        self.phone_number = ""
        self.user_name = ""
        
        # Setup UI
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🏥 Hospital Appointment Bot",
            font=("Arial", 18, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Setup Panel
        self.setup_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        self.setup_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            self.setup_frame,
            text="Setup",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Phone Number
        tk.Label(
            self.setup_frame,
            text="Phone Number:",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.phone_entry = tk.Entry(
            self.setup_frame,
            font=("Arial", 12),
            width=40
        )
        self.phone_entry.insert(0, "919876543210")
        self.phone_entry.pack(pady=(0, 15))
        
        # User Name
        tk.Label(
            self.setup_frame,
            text="Your Name:",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.name_entry = tk.Entry(
            self.setup_frame,
            font=("Arial", 12),
            width=40
        )
        self.name_entry.insert(0, "Test User")
        self.name_entry.pack(pady=(0, 20))
        
        # Start Button
        start_btn = tk.Button(
            self.setup_frame,
            text="Start Chat",
            font=("Arial", 12, "bold"),
            bg="#667eea",
            fg="white",
            cursor="hand2",
            command=self.start_chat,
            padx=20,
            pady=10
        )
        start_btn.pack()
        
        # Chat Frame (hidden initially)
        self.chat_frame = tk.Frame(self.root, bg="white")
        
        # Chat Header
        chat_header = tk.Frame(self.chat_frame, bg="#667eea", height=60)
        chat_header.pack(fill=tk.X)
        chat_header.pack_propagate(False)
        
        self.user_info_label = tk.Label(
            chat_header,
            text="",
            font=("Arial", 12, "bold"),
            bg="#667eea",
            fg="white"
        )
        self.user_info_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        reset_btn = tk.Button(
            chat_header,
            text="Reset",
            font=("Arial", 10),
            bg="#f0f0f0",
            cursor="hand2",
            command=self.reset_chat,
            padx=15,
            pady=5
        )
        reset_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Messages Area
        self.messages_text = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="#f5f5f5",
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.messages_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags for styling
        self.messages_text.tag_config("user", foreground="#667eea", font=("Arial", 11, "bold"))
        self.messages_text.tag_config("bot", foreground="#333333", font=("Arial", 11))
        self.messages_text.tag_config("timestamp", foreground="#888888", font=("Arial", 9))
        
        # Input Area
        input_frame = tk.Frame(self.chat_frame, bg="white", padx=10, pady=10)
        input_frame.pack(fill=tk.X)
        
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=40
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 11, "bold"),
            bg="#667eea",
            fg="white",
            cursor="hand2",
            command=self.send_message,
            padx=20,
            pady=5
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Info Panel
        info_frame = tk.Frame(self.root, bg="white", padx=15, pady=15)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(
            info_frame,
            text="💡 Try saying:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        suggestions = [
            "• I want to book an appointment",
            "• Book appointment for tomorrow",
            "• Check availability"
        ]
        
        for suggestion in suggestions:
            tk.Label(
                info_frame,
                text=suggestion,
                font=("Arial", 9),
                bg="white",
                fg="#555"
            ).pack(anchor=tk.W, pady=2)
    
    def start_chat(self):
        self.phone_number = self.phone_entry.get().strip()
        self.user_name = self.name_entry.get().strip()
        
        if not self.phone_number or not self.user_name:
            return
        
        # Hide setup, show chat
        self.setup_frame.pack_forget()
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Update header
        self.user_info_label.config(text=f"👤 {self.user_name} ({self.phone_number})")
        
        # Add welcome message
        self.add_message(
            "👋 Hi! I'm your hospital appointment assistant. How can I help you today?",
            is_user=False
        )
        
        self.message_entry.focus()
    
    def reset_chat(self):
        self.chat_frame.pack_forget()
        self.setup_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Clear messages
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.delete(1.0, tk.END)
        self.messages_text.config(state=tk.DISABLED)
        
        # Clear session
        appointment_manager.clear_session(self.phone_number)
    
    def add_message(self, text, is_user=False):
        self.messages_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%I:%M %p")
        
        if is_user:
            self.messages_text.insert(tk.END, f"\n[You] ", "user")
        else:
            self.messages_text.insert(tk.END, f"\n[Bot] ", "bot")
        
        self.messages_text.insert(tk.END, f"{text}\n", "bot" if not is_user else "user")
        self.messages_text.insert(tk.END, f"  {timestamp}\n", "timestamp")
        
        self.messages_text.config(state=tk.DISABLED)
        self.messages_text.see(tk.END)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Add user message
        self.add_message(message, is_user=True)
        self.message_entry.delete(0, tk.END)
        
        # Process message
        response = self.handle_message(message)
        
        # Add bot response
        self.root.after(500, lambda: self.add_message(response, is_user=False))
    
    def handle_message(self, text):
        """Handle incoming message and return bot response"""
        session = appointment_manager.get_session(self.phone_number)
        
        # Check if we are in a conversation flow
        if session["step"] != "idle":
            return self.handle_flow_step(text, session)
        
        # If idle, use AI to parse intent
        parsed = ai_service.parse_intent(text)
        print(f"Parsed intent for {self.phone_number}: {parsed}")
        
        if parsed["intent"] == "book_appointment":
            appointment_manager.update_session(self.phone_number, {
                "step": "awaiting_date",
                "tempData": {
                    "userName": self.user_name,
                    "date": parsed["entities"].get("date")
                }
            })
            
            # If we already have the date from the initial message
            if parsed["entities"].get("date"):
                appointment_manager.update_session(self.phone_number, {"step": "awaiting_time"})
                return "Please provide the time for your appointment."
            else:
                return "Sure! What date would you like to book? (YYYY-MM-DD)"
        else:
            # Default response
            return parsed.get("response", "I can help you book an appointment. Just say 'Book appointment'.")
    
    def handle_flow_step(self, text, session):
        """Handle conversation flow steps"""
        if session["step"] == "awaiting_date":
            # Validate date format
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', text):
                return "Invalid date format. Please use YYYY-MM-DD."
            
            appointment_manager.update_session(self.phone_number, {
                "tempData": {**session["tempData"], "date": text},
                "step": "awaiting_time"
            })
            return "Great. What time? (HH:mm)"
        
        elif session["step"] == "awaiting_time":
            # Validate time format
            if not re.match(r'^\d{2}:\d{2}$', text):
                return "Invalid time format. Please use HH:mm."
            
            # Check availability
            date = session["tempData"]["date"]
            is_available = appointment_manager.check_availability(date, text)
            
            if not is_available:
                return "Sorry, that slot is taken. Please choose another time."
            
            # Book the appointment
            appointment = appointment_manager.create_appointment(
                self.phone_number,
                session["tempData"]["userName"],
                date,
                text
            )
            
            appointment_manager.clear_session(self.phone_number)
            return f"✅ Appointment confirmed for {date} at {text}. ID: {appointment['id']}"
        
        return "Something went wrong. Please try again."

def main():
    root = tk.Tk()
    app = WhatsAppBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
