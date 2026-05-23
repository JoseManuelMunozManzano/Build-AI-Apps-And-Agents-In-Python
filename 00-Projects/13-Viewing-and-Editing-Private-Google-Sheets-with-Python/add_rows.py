import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_PRIVATE_ID = os.getenv("SPREADSHEET_PRIVATE_ID")
SHEET_PRIVATE_NAME = os.getenv("SHEET_PRIVATE_NAME")


def add_spreadsheet_data(rows):
    # credenciales, usando Google Service Accounts y un scope de spreadsheet.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    
    # rows es una lista de listas.
    body = {'values': rows}
    
    # valueInputOption puede tener distintos valores, como
    #      RAW          --> los valores crudos
    #      USER_ENTERED --> fórmulas de Excel
    #
    # Ejemplo con USER_ENTERED
    # results = service.spreadsheets().values().append(
    #     spreadsheetId=SPREADSHEET_PRIVATE_ID, range=SHEET_PRIVATE_NAME, valueInputOption='USER_ENTERED', body=body).execute()
    
    results = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_PRIVATE_ID, range=SHEET_PRIVATE_NAME, valueInputOption='RAW', body=body).execute()    
    
    return results


# Pasamos una lista de listas (separadas por coma)
output = add_spreadsheet_data([['Bill Spencer', 'bill@gmail.com', 'Premium'],
                      ['Bill Spencer', 'bill@gmail.com', 'Basic']])
                    #   ['Bill Spencer', 'bill@gmail.com', '=CONTARA(A1:A5)']])
print(output)