import os
import sys

from config_dev import config as config_dev
from config_test import config as config_test
from config_test_travis import config as config_test_travis

config = config_dev  # pylint: disable=C0103

if os.environ.get('TRAVIS'):
  config = config_test_travis  # pylint: disable=C0103
elif hasattr(sys, '_called_from_test'):
  config = config_test  # pylint: disable=C0103

print('config', config)

# NB for production, empty this file,
# then copy and paste config_prod.py into this file instead.
# Then, update mail_sender and mail_password.
