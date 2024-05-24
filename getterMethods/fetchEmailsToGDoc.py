import os.path
import imaplib
import email
from email.header import decode_header
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time

# Your email credentials
username = 'your_email_address'
password = 'your_app_password'

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']

def decode_body(body):
    try:
        return body.decode()
    except UnicodeDecodeError:
        try:
            return body.decode('latin-1')
        except UnicodeDecodeError:
            return body.decode('utf-8', errors='ignore')

def authenticate_google_docs():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

def create_google_doc(service):
    # Create a new Google Doc
    doc = service.documents().create(body={'title': 'Email Fetcher Output'}).execute()
    return doc['documentId']

def write_to_google_doc(service, doc_id, content):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': content
            }
        }
    ]
    result = service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

def fetch_emails(service, doc_id):
    # Connect to the Gmail IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to your account
    imap.login(username, password)

    # Select the mailbox you want to check (inbox in this case)
    imap.select("inbox")

    # Search for all emails in the mailbox
    status, messages = imap.search(None, "ALL")

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    content = ""

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                date = msg.get("Date")
                content += f"Date: {date}\nFrom: {from_}\nSubject: {subject}\n"
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" not in content_disposition:
                            if content_type == "text/plain" or content_type == "text/html":
                                body = part.get_payload(decode=True)
                                body = decode_body(body)
                                content += f"Body:\n{body}\n{'-'*50}\n"
                                break
                else:
                    body = msg.get_payload(decode=True)
                    body = decode_body(body)
                    content += f"Body:\n{body}\n{'-'*50}\n"

    write_to_google_doc(service, doc_id, content)

    imap.close()
    imap.logout()

def main():
    creds = authenticate_google_docs()
    service = build('docs', 'v1', credentials=creds)
    doc_id = create_google_doc(service)
    while True:
        print("Checking for new emails...")
        fetch_emails(service, doc_id)
        time.sleep(1800)  # Wait for 30 minutes before checking again

if __name__ == "__main__":
    main()
