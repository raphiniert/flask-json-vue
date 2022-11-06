import json
import pytest

from flask.config import Config
from flaskjsonvue import create_app
from flaskjsonvue.db import db, setup_engine, list_db_models
from flaskjsonvue.models import Demo


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

        # load test data from json files
        for name, cls in list_db_models():
            import_dir = "tests/data"
            import_file = f"{import_dir}/{name.lower()}.json"
            with open(import_file) as f:
                new_objects = [cls(**o) for o in json.load(f)]
                db.session.add_all(new_objects)
                db.session.commit()

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
