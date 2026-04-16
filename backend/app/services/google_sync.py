import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_service():
    base_path = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_path, 'token.json')
    secret_path = os.path.join(base_path, 'client_secret.json')

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

if __name__ == "__main__":
    print("🔐 Attempting to connect to Google Services...")
    try:
        service = get_google_service()
        print("✅ Success! You are now connected to the Google Sheets API.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
