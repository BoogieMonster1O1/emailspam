import os
import base64
import csv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, sender, message, name):
    sent_message = service.users().messages().send(userId='me', body=message).execute()
    print("Message sent successfully to", name)

def main():
    creds = gmail_authenticate()
    service = build('gmail', 'v1', credentials=creds)

    parsed_data = []
    with open('output.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parsed_data.append(row)

    departments = sorted(set(row['Department'] for row in parsed_data))

    print("Available departments:")
    for i, department in enumerate(departments, start=1):
        print(f"{i}. {department}")
    
    choice = int(input("Select a department number: ")) - 1
    selected_department = departments[choice]

    filtered_data = [row for row in parsed_data if row['Department'] == selected_department]
    sorted_data = sorted(filtered_data, key=lambda x: x['USN'])

    sender_email = "shrishvd.cy23@rvce.edu.in"
    subject_template = "{name}, got a minute?"

    with open("email.html", "r") as file:
        html_content = file.read()

    for person in sorted_data:
        name_title_case = person['Name'].title()
        subject = subject_template.replace('{name}', name_title_case)
        html_message = html_content.replace('{name}', name_title_case)
        message = create_message(sender_email, person['Email'], subject, html_message)
        send_message(service, sender_email, message, name_title_case)

if __name__ == '__main__':
    main()
