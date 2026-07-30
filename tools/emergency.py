("""
Emergency tool - creates high-priority tickets
""")
import uuid
from datetime import datetime

from tools.base_tool import BaseTool
from ai.memory import MemoryManager
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, EMERGENCY_CONTACT_NUMBER, LIFT_ADDRESS
from twilio.rest import Client


class EmergencyTool(BaseTool):

	@property
	def name(self):
		return "emergency"

	def execute(self, arguments):

		memory = MemoryManager()

		ticket = {
			"id": uuid.uuid4().hex,
			"description": arguments.get("description"),
			"priority": arguments.get("priority", "high"),
			"created_at": datetime.utcnow().isoformat() + "Z",
			"status": "emergency"
		}

		memory.add_ticket(ticket)

		# Trigger Outbound Emergency Call
		try:
			client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
			
			address = arguments.get("address", "an unknown location")
			twiml = f"<Response><Say>Attention! The caller is in an emergency. The location of the lift is: {address}. Passenger report: {ticket['description']}</Say></Response>"
			
			call = client.calls.create(
				twiml=twiml,
				to=EMERGENCY_CONTACT_NUMBER,
				from_=TWILIO_PHONE_NUMBER
			)
			print(f"Triggered emergency call! SID: {call.sid}")
		except Exception as e:
			print(f"Failed to trigger emergency call: {e}")

		return {
			"status": "created",
			"ticket": ticket
		}

