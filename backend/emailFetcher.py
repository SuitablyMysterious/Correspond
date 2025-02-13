from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
import email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SERVICE_ACCOUNT_FILE = "path/to/credentials.json"  # Update this!

def get_gmail_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("gmail", "v1", credentials=creds)

def fetch_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=5).execute()
    messages = results.get("messages", [])

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        msg_snippet = msg_data["snippet"]
        msg_payload = msg_data["payload"]
        headers = msg_payload["headers"]

        sender = next(h["value"] for h in headers if h["name"] == "From")
        subject = next(h["value"] for h in headers if h["name"] == "Subject")

        body = "No Body"
        for part in msg_payload.get("parts", []):
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode()

        print(f"From: {sender}\nSubject: {subject}\nSnippet: {msg_snippet}\nBody: {body[:200]}...\n")
