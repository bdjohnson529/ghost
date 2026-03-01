import os
import logging
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger("ghost.scan")

# --- CONFIGURATION ---
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def connect_to_email():
    # Connect to the server
    logger.info("connect_to_email called, IMAP_SERVER=%s", IMAP_SERVER or "(not set)")
    if not IMAP_SERVER:
        raise ValueError("IMAP_SERVER environment variable is not set")
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("EMAIL_USER or EMAIL_PASS environment variable is not set")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    logger.info("Connected to IMAP and selected inbox")
    return mail

def find_services():
    logger.info("find_services called")

    mail = connect_to_email()
    
    # Search for emails with "Welcome" in the subject
    # You can expand this: 'OR (SUBJECT "Welcome") (SUBJECT "Confirm")'
    status, messages = mail.search(None, '(SUBJECT "Welcome")')
    logger.info("IMAP search status=%s", status)
    
    email_ids = messages[0].split() if messages[0] else []
    services_found = set() # Use a set to avoid duplicates

    logger.info("Scanning %d emails...", len(email_ids))

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
    logger.info("find_services completed, found %d services", len(services_found))
    return services_found

if __name__ == "__main__":
    found = find_services()
    print("\n--- Potential Services Found ---")
    for s in sorted(found):
        print(s)