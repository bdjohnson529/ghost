import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- CONFIGURATION ---
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def connect_to_email():
    # Connect to the server
    print("connect to email called")
    print(IMAP_SERVER)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail

def find_services():
    print("find services")

    mail = connect_to_email()
    
    # Search for emails with "Welcome" in the subject
    # You can expand this: 'OR (SUBJECT "Welcome") (SUBJECT "Confirm")'
    status, messages = mail.search(None, '(SUBJECT "Welcome")')
    
    email_ids = messages[0].split()
    services_found = set() # Use a set to avoid duplicates

    print(f"Scanning {len(email_ids)} emails...")

    for e_id in email_ids:
        # Fetch only the header (faster than fetching the whole email)
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Get the 'From' field (e.g. "Under Armour <support@ua.com>")
                sender = msg.get("From")
                services_found.add(sender)

    mail.logout()
    return services_found

if __name__ == "__main__":
    found = find_services()
    print("\n--- Potential Services Found ---")
    for s in sorted(found):
        print(s)