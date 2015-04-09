from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP

config = {
    'mail_sender': 'support@example.com',
    'mail_password': 'wW6Yd6jJHBVilJHX',
    'mail_username': 'admin@example.com',
    'mail_server': 'smtp.mandrillapp.com',
    'mail_port': 587,
}


def send_mail(subject, recipient, body):
    """
    Send an email.
    """

    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = config['mail_sender']
    msg['To'] = recipient
    try:
        conn = SMTP(config['mail_server'])
        conn.set_debuglevel(False)
        conn.login(config['mail_username'], config['mail_password'])
        conn.sendmail(msg['To'], [recipient], msg.as_string())
    finally:
        if conn:
            conn.close()
