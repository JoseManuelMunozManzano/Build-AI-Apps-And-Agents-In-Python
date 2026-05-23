import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_PRIVATE_ID = os.getenv("SPREADSHEET_PRIVATE_ID")
SHEET_PRIVATE_NAME = os.getenv("SHEET_PRIVATE_NAME")


def get_spreadsheet_data():
    # credenciales, usando Google Service Accounts y un scope de spreadsheet.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    all_rows = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_PRIVATE_ID, range=SHEET_PRIVATE_NAME).execute()['values']
    
    return all_rows


all_rows = get_spreadsheet_data()
print(all_rows)