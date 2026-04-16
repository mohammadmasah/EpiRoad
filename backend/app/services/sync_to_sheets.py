import json
import os
from google_sync import get_google_service

def update_spreadsheet():
    # Detect path
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, 'jobs_data.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("❌ JSON file not found.")
        return

    try:
        service = get_google_service()
        
        # 1. CREATE A BRAND NEW FILE (No IDs needed)
        print("Creating a brand new spreadsheet...")
        spreadsheet_body = {'properties': {'title': 'EpiRoad Final Results'}}
        new_file = service.spreadsheets().create(body=spreadsheet_body).execute()
        new_id = new_file.get('spreadsheetId')
        
        # 2. PREPARE THE DATA
        values = [["Job Title", "Company", "Location", "Link"]]
        for job in jobs:
            values.append([job.get('title'), job.get('company'), job.get('location'), job.get('link')])

        # 3. UPLOAD DATA
        print(f"📤 Uploading {len(jobs)} jobs to the new sheet...")
        service.spreadsheets().values().update(
            spreadsheetId=new_id,
            range="Sheet1!A1",
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
        
        print(f"✅ SUCCESS! New file created.")
        print(f"🔗 LINK: https://docs.google.com/spreadsheets/d/{new_id}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_spreadsheet()
