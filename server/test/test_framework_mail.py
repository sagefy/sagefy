
from framework.mail import config, send_mail


def test_send_mail_as_test():
  subject = 'This is a test mail'
  recipient = 'test@example.com'
  body = 'This is a test mail'
  assert send_mail(subject, recipient, body) is True


def test_send_mail_as_prod_no_connect():
  prev_config_test = config['test']
  config['test'] = False
  subject = 'This is a test mail'
  recipient = 'test@example.com'
  body = 'This is a test mail'
  assert send_mail(subject, recipient, body) is False
  config['test'] = prev_config_test
