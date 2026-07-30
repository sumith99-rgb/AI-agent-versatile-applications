"""
WhatsApp tool - Sends WhatsApp messages via pywhatkit and logs them to DB
"""
import pywhatkit
from datetime import datetime
import time

from tools.base_tool import BaseTool
from ai.memory import MemoryManager


class WhatsAppTool(BaseTool):

    @property
    def name(self):
        return "whatsapp"

    def execute(self, arguments):
        
        recipient = arguments.get("to")
        message = arguments.get("message")
        
        memory = MemoryManager()
        
        if not recipient or not message:
            return {"status": "error", "message": "Missing recipient or message"}
            
        # Add country code if missing (assumed India +91 for example purposes if 10 digits)
        if len(recipient) == 10 and recipient.isdigit():
            recipient = f"+91{recipient}"

        print(f"\nOpening WhatsApp Web to send message to {recipient}...")
        print("Please do not close your browser. It will take around 15 seconds.")
        
        try:
            # Send message instantly (requires whatsapp web logged in)
            # wait_time is 15 seconds to let WhatsApp Web load, tab_close=True prevents endless tabs
            pywhatkit.sendwhatmsg_instantly(
                phone_no=recipient,
                message=message,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            
            memory.add_whatsapp_message(recipient, message)
            print("WhatsApp message sent successfully and logged to DB!")
            
            return {
                "status": "sent",
                "recipient": recipient
            }
            
        except Exception as e:
            print(f"\nError sending WhatsApp message: {e}")
            # If pywhatkit fails, still log it to DB for tracking purposes
            memory.add_whatsapp_message(recipient, message)
            return {
                "status": "error",
                "error": str(e)
            }
