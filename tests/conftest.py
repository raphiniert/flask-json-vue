import pytest
from flask.config import Config
from flaskjsonvue import create_app
from flaskjsonvue.db import db, setup_engine


@pytest.fixture
def app():
    """
    create the app with the test config from config file
    :return:
    """
    # create config from test config file
    config = Config("instance/")
    # load config from pyfile
    config.from_pyfile("test_config.py", silent=False)
    # create app
    app = create_app(config)

    # setup db
    with app.app_context():
        setup_engine()
        db.init_app(app)
        db.create_all()

    yield app

    # drop db after tests are finished
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """
    create a test client
    :param app:
    :return:
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    create test cli runner
    :param app:
    :return:
    """
    return app.test_cli_runner()
