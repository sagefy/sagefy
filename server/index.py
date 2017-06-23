"""
Welcome to Sagefy.
"""
# flake8: noqa

from config import config
import framework.index as framework
framework.update_config(config)

from framework.database import setup_db
setup_db()

import routes.public
import routes.user
import routes.notice
import routes.topic
import routes.post
import routes.follow
import routes.user_subjects
import routes.card
import routes.unit
import routes.subject
import routes.search
import routes.next
import routes.sitemap

from framework.index import serve
