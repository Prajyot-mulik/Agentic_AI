import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    SCOPES
                )
                creds = flow.run_local_server(port=0)  # Let the system choose a random port
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def fetch_unread_emails(self):
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            email = {
                'id': msg['id'],
                'subject': next(header['value'] for header in msg_data['payload']['headers'] if header['name'] == 'Subject'),
                'body': msg_data['snippet'],
                'from': next(header['value'] for header in msg_data['payload']['headers'] if header['name'] == 'From')
            }
            emails.append(email)
        return emails

    def send_reply(self, original_email, response_text):
        try:
            message = {
                'raw': self._create_message(original_email, response_text)
            }
            self.service.users().messages().send(userId='me', body=message).execute()
            print("Response sent successfully!")
        except Exception as e:
            print(f"Failed to send response: {e}")

    def _create_message(self, original_email, response_text):
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['To'] = original_email['from']  # Use the 'from' key
        msg['Subject'] = f"Re: {original_email['subject']}"
        msg.attach(MIMEText(response_text, 'plain'))

        return base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')