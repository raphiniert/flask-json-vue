import click
import json
import logging

from flask.cli import with_appcontext

from flaskjsonvue.db import list_db_models

logger = logging.getLogger("flaskjsonvue")


@click.command("export-json")
@click.option(
    "--export-dir",
    type=str,
    default="flaskjsonvue/static/json",
    help="Directory to write JSON files.",
)
@click.option(
    "--model",
    type=str,
    default=None,
    help="model class name to export",
)
@with_appcontext
def export_json(export_dir: str, model: str):
    # list all model classes extending db.Model
    db_model_classes = [obj for name, obj in list_db_models()]

    # filter by model name if provided
    if model:
        model = model.lower()
        # logging.info(f"Filtering by model: {model}")
        click.echo(f"Filtering by model: {model}")
        db_model_classes = [
            obj for obj in db_model_classes if obj.__name__.lower() == model
        ]

    for db_model_class in db_model_classes:
        obj_list = []
        model_name = db_model_class.__name__.lower()

        for obj in db_model_class.query.all():
            obj_list.append(obj.json.get("data"))
        if obj_list:
            json_path = f"{export_dir}/{model_name}.json"
            click.echo(f"Exporting {model_name} to: {json_path}")
            # logging.info(f"Exporting {model_name} to: {json_path}")
            with open(json_path, "w") as f:
                # dump utf-8 json
                json.dump(obj_list, f, indent=4, ensure_ascii=False)
                click.echo(f"Exported {model_name}.")
                # logging.info(f"Exported {model_name}.")
        else:
            click.echo(f"Could not find any {model_name} objects to export.")
            # logging.info(f"Could not find any {model_name} objects to export.")
    else:
        click.echo(f"No models found.")
