import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SPREADSHEET_API_KEY = os.getenv("GOOGLE_SPREADSHEET_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_spreadsheet_data():
    """Fetch spreadsheet data"""
    service = build('sheets', 'v4', developerKey=GOOGLE_SPREADSHEET_API_KEY)
    all_rows = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()['values']
    # El fichero last_row.txt tiene que existir la primera vez que se ejecuta este script con el valor 0
    with open('last_row.txt') as file:
        last_row = int(file.read())
    new_rows = all_rows[last_row:]
    headers = all_rows[0]
    return all_rows, new_rows, headers

def summarize_with_ai(text):
    system_prompt = """
    You are a helpful assistant that summarizes spreadsheet data.
    You will receive new rows that were added to a Google Spreadsheet. 
    Please provide a clear, concise summary of this data
    """
    model = init_chat_model("gemini-3-flash-preview", api_key=GEMINI_API_KEY, model_provider="google_genai")
    message = [{"role": "system", "content": system_prompt},
               {"role": "user", "content": f"Here are the new rows from the spreadsheet \n {text}"}]
    response = format_response(model.invoke(message).content)
    return response

def send_email(subject, body):
    """Send email with the summary."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"Email sent successfully to {RECIPIENT_EMAIL}")

def format_response(content: str | list):
    """Format the IA response"""
    if isinstance(content, list):
        text = " ".join(part.get("text", "") for part in content)
    else:
        text = content
    return text


all_rows, new_rows, headers = get_spreadsheet_data()
total_rows = len(all_rows)
with open("last_row.txt", 'w') as file:
    file.write(str(total_rows))

message = f"Headers: {headers} \nNew rows: {new_rows}"
print(message)
summary = summarize_with_ai(message)

body = f"Here is today's summary \n\n{summary}\n\n Thanks!"
send_email("Daily Spreadsheet Summary", body)

print("ALL_ROWS", all_rows)
print("NEW_ROWS", new_rows)
print(summary)