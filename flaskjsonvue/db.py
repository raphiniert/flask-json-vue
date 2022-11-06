import click
import inspect
import json

from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
Base = declarative_base()


def setup_engine():
    engine = create_engine(
        current_app.config.get("SQLALCHEMY_DATABASE_URI"),
    )
    Base.metadata.reflect(engine)


def list_db_models():
    from flaskjsonvue import models

    #  return list of all member names that extend db.Model
    return [
        (name, obj)
        for name, obj in inspect.getmembers(models)
        if hasattr(obj, "__mro__") and db.Model in obj.__mro__
    ]


@click.command("init-db")
@click.option(
    "--auto-import/--no-auto-import", default=False, help="Auto import all models."
)
@click.option(
    "--import-dir",
    default="flaskjsonvue/static/json",
    help="Directory to import models from.",
)
@click.pass_context
@with_appcontext
def init_db(ctx: click.Context, auto_import: bool, import_dir: str):
    db.drop_all()
    click.echo(f"Dropped all tables.")
    db.create_all()
    click.echo(f"Created all tables.")
    click.echo(f"Initialized database.")
    if auto_import:
        for name, cls in list_db_models():
            import_file = f"{import_dir}/{name.lower()}.json"
            # check if file exists
            try:
                with open(import_file) as f:
                    click.echo(f"Importing {name} objects from {import_file}")
                    data = json.load(f)
                    for item in data:
                        new_obj = cls(**item)
                        db.session.add(new_obj)
                        db.session.commit()
                        click.echo(f"Imported {new_obj}.")
            except FileNotFoundError:
                click.echo(f"File {import_file} not found.")
