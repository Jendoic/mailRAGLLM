import imaplib
import os
import email
from email.header import decode_header
import time
import csv

# Define your credentials
username = 'your_email_address'
password = 'your_app_password'

# Function to fetch emails from a specific folder
def fetch_emails_from_folder(mail, folder, txt_file, csv_writer, processed_ids):
    mail.select(folder)

    # Search for all emails in the selected folder
    status, messages = mail.search(None, "ALL")
    if status != 'OK':
        print(f"Failed to retrieve emails from {folder}")
        return

    # Convert messages to a list of email IDs
    mail_ids = messages[0].split()

    # Fetch each email by ID, only if it's not processed yet
    for mail_id in mail_ids:
        if mail_id in processed_ids:
            continue

        status, msg_data = mail.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                # Decode the email sender
                from_ = msg.get("From")

                # Decode the email date
                date = msg.get("Date")

                # Initialize variable to hold plain text content
                plain_text = ""

                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        # Get the email body (plain text part)
                        if part.get_content_type() == "text/plain":
                            plain_text = get_decoded_payload(part)
                            break  # Stop after finding the first plain text part
                else:
                    # Get the email body for non-multipart emails
                    if msg.get_content_type() == "text/plain":
                        plain_text = get_decoded_payload(msg)

                # Write to TXT file
                txt_file.write(f"Folder: {folder}\n")
                txt_file.write(f"Subject: {subject}\n")
                txt_file.write(f"From: {from_}\n")
                txt_file.write(f"Date: {date}\n")
                txt_file.write(f"Body: {plain_text}\n")
                txt_file.write("\n" + "="*50 + "\n\n")

                # Write to CSV file
                csv_writer.writerow([folder, subject, from_, plain_text, date])

                # Add the mail ID to the processed list
                processed_ids.add(mail_id)

# Helper function to decode email payload with different encodings
def get_decoded_payload(part):
    payload = part.get_payload(decode=True)
    encodings = ['utf-8', 'latin-1', 'windows-1252']
    for enc in encodings:
        try:
            return payload.decode(enc)
        except UnicodeDecodeError:
            continue
    return payload.decode('utf-8', errors='replace')  # Fall back to UTF-8 with replacement

# Load processed email IDs from file
def load_processed_ids(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(line.strip() for line in f)
    return set()

# Save processed email IDs to file
def save_processed_ids(filename, processed_ids):
    with open(filename, "w") as f:
        for mail_id in processed_ids:
            f.write(f"{mail_id}\n")

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to your account
mail.login(username, app_password)

# List of folders to fetch emails from
folders = ["inbox", "[Gmail]/Spam", "[Gmail]/Drafts"]

# Load processed email IDs
processed_ids_filename = "processed_ids.txt"
processed_ids = load_processed_ids(processed_ids_filename)

# Open files for writing
with open("emails.txt", "a", encoding='utf-8') as txt_file, open("emails.csv", "a", newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write CSV header if the file is empty
    if os.stat("emails.csv").st_size == 0:
        csv_writer.writerow(["Folder", "Subject", "From", "Body", "Date"])

    # Fetch email data and save to files in an infinite loop
    try:
        while True:
            for folder in folders:
                fetch_emails_from_folder(mail, folder, txt_file, csv_writer, processed_ids)

            # Save processed email IDs
            save_processed_ids(processed_ids_filename, processed_ids)

            # Sleep for a specified amount of time before checking again (e.g., 3600 seconds for 1 hour)
            time.sleep(3600)
    finally:
        # Ensure we close the connection and logout even if an error occurs or we break the loop
        mail.close()
        mail.logout()
