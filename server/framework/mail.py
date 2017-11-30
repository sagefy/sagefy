from email.mime.text import MIMEText
from smtplib import SMTP
from config import config

FOOTER_TEXT = """


This is a transactional email from Sagefy.
We are required to notify you of sign ups, password changes,
and any security incidents while you have an account.
If you would like to unsubscribe from other types of notices
or if you would like to delete your account,
please reply to this email and let us know.
We will fulfill your request within 10 business days.
"""


def send_mail(subject, recipient, body):
  """
  Send an email.
  """

  if config['test']:
    return True
  sent = False
  msg = MIMEText(body + FOOTER_TEXT, 'plain')
  msg['Subject'] = subject
  msg['From'] = config['mail_sender']
  msg['To'] = recipient
  conn = None
  try:
    conn = SMTP(
      config['mail_server'],
      config['mail_port'],
      timeout=5
    )
    conn.set_debuglevel(False)
    conn.login(config['mail_username'], config['mail_password'])
    conn.sendmail(msg['To'], [recipient], msg.as_string())
    sent = True
  except:
    pass
  finally:
    if conn:
      conn.close()
  return sent
