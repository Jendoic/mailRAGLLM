import imaplib
import email
from email.header import decode_header
import time

# Your email credentials
username = 'your_email_address'
password = 'your_app_password'

def decode_body(body):
    try:
        return body.decode()
    except UnicodeDecodeError:
        try:
            return body.decode('latin-1')
        except UnicodeDecodeError:
            return body.decode('utf-8', errors='ignore')

def fetch_emails():
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
                print(f"Date: {date}")
                print(f"From: {from_}")
                print(f"Subject: {subject}")
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" not in content_disposition:
                            if content_type == "text/plain" or content_type == "text/html":
                                body = part.get_payload(decode=True)
                                body = decode_body(body)
                                print(f"Body:\n{body}\n{'-'*50}")
                                break
                else:
                    body = msg.get_payload(decode=True)
                    body = decode_body(body)
                    print(f"Body:\n{body}\n{'-'*50}")
    
    imap.close()
    imap.logout()

def main():
    # Initial fetch
    fetch_emails()
    # Periodically check for new emails
    while True:
        print("Checking for new emails...")
        fetch_emails()
        time.sleep(1800)  # Wait for 30 minutes before checking again

if __name__ == "__main__":
    main()
