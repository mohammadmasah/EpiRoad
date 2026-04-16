import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def sync_data():
    # 1. Configuration
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    DATA_FILE = 'jobs_data.json'
    
    # Using your Spreadsheet ID
    SPREADSHEET_ID = '1lzeeh4x981Icoebbr8jNifSMJ7Qlgt1jgFIBctWOH4s'

    # 2. Authentication
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return

    # 3. Load Scraped Data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    except Exception as e:
        print(f"❌ Data Loading Error: {e}")
        return

    # 4. Prepare Data
    values = [["Title", "Company", "Location", "Contract", "Link"]]
    job_list = jobs if isinstance(jobs, list) else jobs.values()
    
    for job in job_list:
        values.append([
            job.get('title', 'N/A'),
            job.get('company', 'N/A'),
            job.get('location', 'N/A'),
            job.get('contract', 'N/A'),
            job.get('link', 'N/A')
        ])

    # 5. Update the EXISTING Spreadsheet
    try:
        body = {'values': values}
        # First we update the sheet
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, 
            range="Sheet1!A1",
            valueInputOption="RAW", 
            body=body
        ).execute()

        print(f"✅ Success! {len(values)-1} jobs synchronized to your existing sheet.")
        print(f"🔗 View here: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
    except Exception as e:
        print(f"❌ Google API Error: {e}")

if __name__ == "__main__":
    sync_data()