("""
Ticket tool - stores tickets in MemoryManager
""")
import uuid
from datetime import datetime

from tools.base_tool import BaseTool
from ai.memory import MemoryManager
from config import COMPANY_SUPPORT_EMAIL
from tools.email import EmailTool
from tools.whatsapp import WhatsAppTool


class TicketTool(BaseTool):

	@property
	def name(self):
		return "ticket"

	def execute(self, arguments):

		memory = MemoryManager()

		ticket = {
			"id": uuid.uuid4().hex,
			"description": arguments.get("description"),
			"created_at": datetime.utcnow().isoformat() + "Z",
			"status": "open"
		}

		memory.add_ticket(ticket)

		# We must run these in a separate background thread so it doesn't block the 15-second Twilio Webhook timeout!
		import threading

		def send_notifications():
			# 1. Notify the Company via Email
			email_tool = EmailTool()
			email_tool.execute({
				"to": COMPANY_SUPPORT_EMAIL,
				"subject": f"New Ticket Raised: {ticket['id']}",
				"body": f"A new ticket has been raised by a customer.\n\nTicket ID: {ticket['id']}\nDescription: {ticket['description']}"
			})

			# 2. Notify the Customer via WhatsApp (if phone number is known)
			user_phone = memory.get_user("phone")
			if user_phone:
				whatsapp_tool = WhatsAppTool()
				whatsapp_tool.execute({
					"to": user_phone,
					"message": f"Your ticket has been successfully created. Ticket ID: {ticket['id']}\nDescription: {ticket['description']}"
				})
				
		threading.Thread(target=send_notifications).start()

		return {
			"status": "created",
			"ticket": ticket
		}

