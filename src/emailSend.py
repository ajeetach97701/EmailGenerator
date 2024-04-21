import os, smtplib
import email.message 


def send_email(to_email, subject, message):
    smtp_server = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT'))  # Convert to int
    sender_email = os.getenv('EMAIL_DEV')
    password = os.getenv('EMAIL_PASSWORD')

    msg = email.message.Message()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, password)
    smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    smtp.quit()
    print("Successfully sent email to", to_email)
