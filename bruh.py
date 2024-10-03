import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, sender, message):
    """Send an email message."""
    try:
        sent_message = service.users().messages().send(userId=sender, body=message).execute()
        print(f"Message sent successfully: {sent_message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def main():
    # Authenticate and create the Gmail API service
    creds = gmail_authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # Sender, receiver and subject of the email
    sender_email = "shrishvd.cy23@rvce.edu.in"
    receiver_email = "sakshamgupta.cy23@rvce.edu.in"
    subject = "{name}, got a minute?"

    # Read the email.html content
    with open("email.html", "r") as file:
        html_content = file.read()

    # Create and send the email
    html_content = html_content.replace('{name}', 'Saksham Gupta');
    subject = subject.replace('{name}', 'Saksham Gupta');

    message = create_message(sender_email, receiver_email, subject, html_content)
    send_message(service, sender_email, message)

if __name__ == '__main__':
    main()
