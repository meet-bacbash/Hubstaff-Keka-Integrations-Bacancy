import imaplib
import email
from email.header import decode_header
import os
from datetime import date

todays_date = date.today()


# Function to download email attachments
def download_attachments():
    mail_user = "manthan0404soni@gmail.com"
    mail_pass = "ydbvvkqkcmmbajlm"
    subject_to_find = "Bacancy Technology LLP Work Sessions Report"

    # Connect to the Gmail IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to the account
    imap.login(mail_user, mail_pass)

    # Select the mailbox you want to check (inbox in this case)
    imap.select("inbox")

    # Search for the specific email (based on subject in this example)
    status, messages = imap.search(None, f'(SUBJECT "{subject_to_find}")')

    # Convert the result to a list of email IDs
    email_ids = messages[0].split()

    if email_ids:
        # Fetch the latest email (the last email ID in the list)
        latest_email_id = email_ids[0]

        # Fetch the email by ID
        res, msg = imap.fetch(latest_email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # Parse the email content
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                print(f"Processing the latest email with Subject: {subject}")

                # If the email has multiple parts
                if msg.is_multipart():
                    for part in msg.walk():
                        # If part is an attachment
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                # Download attachment to the Downloads folder
                                filepath = os.path.join("Downloads", filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"Downloaded: {filename}")
                else:
                    print("No attachments found.")
    else:
        print("No email found with the given subject.")

    # Close the connection and logout
    imap.close()
    imap.logout()


# mail_user = "manthan0404soni@gmail.com"
# mail_pass = "ydbvvkqkcmmbajlm"
# subject_to_find = "Bacancy Technology LLP Work Sessions Report"
#
# download_attachments(mail_user, mail_pass, subject_to_find)
