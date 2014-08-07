# via http://stackoverflow.com/a/11158224
import pytest
import os
import sys
import inspect

currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app import create_app
import config


@pytest.fixture(scope='session')
def app(request):
    # For now, use the same config mostly and
    # we'll just create a separate test database
    config.RDB_DB = 'sagefy_test'

    app = create_app(config, debug=True, testing=True)

    # Manage app context for testing
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app
