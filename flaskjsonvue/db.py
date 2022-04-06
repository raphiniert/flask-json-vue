import click
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


@click.command("init-db")
@click.option(
    "--auto-import/--no-auto-import", default=False, help="Auto import all models."
)
@click.pass_context
@with_appcontext
def init_db(ctx: click.Context, auto_import: bool):
    db.drop_all()
    click.echo(f"Dropped all tables.")
    db.create_all()
    click.echo(f"Created all tables.")
    if auto_import:
        raise NotImplementedError(f"auto import is not yet implemented")
        # TODO: import importer
        # ctx.invoke(importer)