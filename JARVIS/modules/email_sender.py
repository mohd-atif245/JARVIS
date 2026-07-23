import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from core.config import GMAIL_SENDER

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_FILE = "credentials/gmail_token.json"
CREDS_FILE = "credentials/gmail_credentials.json"


def _get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs("credentials", exist_ok=True)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def send_email(to: str, subject: str, body: str) -> str:
    try:
        service = _get_gmail_service()
        message = MIMEText(body)
        message["to"] = to
        message["from"] = GMAIL_SENDER
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to} successfully."
    except Exception as e:
        return f"Email failed: {e}"
