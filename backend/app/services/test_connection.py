import json
import os
from google_sync import get_google_service


SPREADSHEET_ID = '1lzeeh4x981lcoebbr8jNifSMJ7Qlgt1jgFIBctWOH4s'
RANGE_NAME = 'Sheet1!A1'

def update_spreadsheet():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, 'jobs_data.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print(f"❌ JSON file not found.")
        return

    values = [["Job Title", "Company", "Location", "Link"]]
    for job in jobs:
        values.append([
            job.get('title', 'N/A'), 
            job.get('company', 'N/A'), 
            job.get('location', 'N/A'), 
            job.get('link', 'N/A')
        ])

    try:
        service = get_google_service()
        sheet = service.spreadsheets()
        
        print(f"📤 Uploading {len(jobs)} jobs to Google Sheets...")
        

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
        
        print(f"✅ SUCCESS! {result.get('updatedCells')} cells updated.")

    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    update_spreadsheet()
