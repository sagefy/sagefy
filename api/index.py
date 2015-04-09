"""
Welcome to Sagefy.
"""

from config import config
import framework.index as framework
framework.update_config(config)

from framework.database import setup_db
setup_db()

import routes.public  # flake8: noqa
import routes.user  # flake8: noqa
import routes.notice  # flake8: noqa
import routes.topic  # flake8: noqa
import routes.follow  # flake8: noqa
import routes.user_sets  # flake8: noqa
import routes.card  # flake8: noqa
import routes.unit  # flake8: noqa
import routes.set  # flake8: noqa
import routes.search  # flake8: noqa
import routes.sequencer  # flake8: noqa

from framework.index import serve  # flake8: noqa
