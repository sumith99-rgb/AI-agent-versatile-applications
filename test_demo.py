import requests
from twilio.rest import Client
import config

def get_ngrok_url():
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except:
        return None

ngrok_url = get_ngrok_url()
if not ngrok_url:
    print("Error: Could not find ngrok. Make sure 'ngrok http 5000' is running in another terminal!")
    exit(1)

print(f"Found ngrok URL: {ngrok_url}")
print(f"Triggering demo call to your cell phone ({config.EMERGENCY_CONTACT_NUMBER})...")

try:
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=config.EMERGENCY_CONTACT_NUMBER,
        from_=config.TWILIO_PHONE_NUMBER,
        url=f"{ngrok_url}/voice"
    )
    print(f"\nSUCCESS! Call initiated! Your cell phone should be ringing right now...")
    print(f"When you answer, you will be talking to your AI!")
except Exception as e:
    print(f"\nFailed to initiate call: {e}")
