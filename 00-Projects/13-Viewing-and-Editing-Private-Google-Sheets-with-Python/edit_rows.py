import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_PRIVATE_ID = os.getenv("SPREADSHEET_PRIVATE_ID")
SHEET_PRIVATE_NAME = os.getenv("SHEET_PRIVATE_NAME")


def update_spreadsheet_data(rows, row_number):
    # credenciales, usando Google Service Accounts y un scope de spreadsheet.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    
    # rows es una lista de listas.
    body = {'values': rows}
    
    # Actualizar una fila (row)
    # Queremos obtener "Hoja 1"!A9:C9
    range_name = f"{SHEET_PRIVATE_NAME}!A{row_number}:C{row_number}"
    
    # Actualizar una celda (cell)
    # range_name = f"{SHEET_PRIVATE_NAME}!A{row_number}"

    results = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_PRIVATE_ID, range=range_name, valueInputOption='RAW', body=body).execute()    
    
    return results


# Pasamos una lista de listas (separadas por coma)
# Actualizar una fila
output = update_spreadsheet_data([['Bob Spencer', 'bob@gmail.com', 'Premium']], 5)

# Actualizar una celda
# output = update_spreadsheet_data([['Jack Spencer']], 5)

print(output)