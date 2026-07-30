"""
Email tool - Sends emails via SMTP and logs them to the SQLite database
"""
import smtplib
from email.message import EmailMessage
import traceback

from tools.base_tool import BaseTool
from ai.memory import MemoryManager
from config import SMTP_EMAIL, SMTP_PASSWORD


class EmailTool(BaseTool):

    @property
    def name(self):
        return "email"

    def execute(self, arguments):
        
        recipient = arguments.get("to")
        subject = arguments.get("subject", "Message from LiftGuard AI")
        body = arguments.get("body")
        
        memory = MemoryManager()
        
        if not recipient or not body:
            return {"status": "error", "message": "Missing recipient or body"}
            
        if not SMTP_EMAIL or SMTP_EMAIL == "your-email@gmail.com":
            print("\nSMTP Configuration missing! Unable to send real email.")
            # Still log it so the user can test the database flow
            memory.add_email(recipient, subject, body)
            return {
                "status": "failed",
                "message": "SMTP not configured. Logged to DB only."
            }
            
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = SMTP_EMAIL
            msg['To'] = recipient

            print(f"\nSending email to {recipient}...")
            
            # Using Gmail's SMTP server by default
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            memory.add_email(recipient, subject, body)
            print("Email sent successfully and logged to DB!")
            
            return {
                "status": "sent",
                "recipient": recipient
            }
            
        except Exception as e:
            print(f"\nError sending email: {e}")
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }
