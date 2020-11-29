import os
import tempfile

import pytest
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')

# Call the factory and pass the test_config to configure the application and database
# for testing instead of using your local development configuration
@pytest.fixture
def application():
    # Create and open a temporary file
    db_fd, db_path = tempfile.mkstemp()

    # Call to the factory
    application = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with application.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield application

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(application):
    return application.test_client()

@pytest.fixture
def runner(application):
    return application.test_cli_runner()