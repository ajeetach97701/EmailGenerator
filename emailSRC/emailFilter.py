

"""
main code that runs

"""

import imaplib
import pprint
import os
from emailSRC.invoke_llm import invoke_llm
from src.emailSend import send_email
from emailSRC.gmail_list import CustomEmailListener
# import psutil 


email =  os.getenv('EMAIL_DEV')
app_password = os.getenv('EMAIL_PASSWORD')
folder = "Inbox"
attachment_dir = "./email_attachments/"


# Email account credentials
EMAIL = os.getenv('EMAIL_DEV')
PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_SERVER = 'imap.gmail.com'  

# Function to check for new emails
def check_for_new_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')  
        status, data = mail.search(None, '(OR (BODY "unsubscribe") (OR (BODY "sale") (BODY "discount")))')

        

        print(status)
        mail_ids = data[0].split()
        
        if mail_ids:
            # run the agent to fetch emails and send it as json to another chain
            
            el = CustomEmailListener(email, app_password, folder, attachment_dir)
            el.login()
            messages= el.scrape()
            print(messages)
            print("message from deff")
            invoke_llm(messages)
            
            
                    
        else:
            print("No new emails.")

        mail.logout()
    except Exception as e:
        print(f"Error checking emails: {e}")

