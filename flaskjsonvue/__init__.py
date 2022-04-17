import os
import logging

from flask import Flask
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", handlers=[RichHandler()]
)

logger = logging.getLogger("flaskjsonvue")


def create_app(test_config=None):
    """
    # TODO: comment create_app
    :param test_config:
    :return:
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        config_file = "config.py"
        app.config.from_pyfile(config_file, silent=True)
        logger.debug(f"Loaded app conifg from {config_file}.")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        logger.debug(f"Loaded app conifg from mapping {test_config}.")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db stuff
    from flaskjsonvue.db import db, setup_engine

    with app.app_context():
        setup_engine()

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # register blueprints
    # api v1
    from flaskjsonvue.api.v1 import demo as api_v1_demo

    app.register_blueprint(api_v1_demo.bp)
    logger.debug(f"Registered api_v1_demo blueprint")
    # add rule to make demo index view func

    # client
    from flaskjsonvue.client import demo as client_demo

    app.register_blueprint(client_demo.bp)
    logger.debug(f"Registred client_demo blueprint")
    # add app url rule to make client demo index root endpoint
    app.add_url_rule("/", endpoint="root", view_func=client_demo.index)

    # custom cli commands
    # db related
    from flaskjsonvue.db import init_db

    app.cli.add_command(init_db)

    return app
