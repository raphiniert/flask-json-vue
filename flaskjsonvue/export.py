import click
import json
import logging

from flaskjsonvue.db import list_db_models

logger = logging.getLogger("flaskjsonvue")


@click.command("export-json")
@click.option(
    "--dirname",
    type=str,
    default="flaskjsonvue/static/json",
    help="Directory to write JSON files.",
)
@click.option(
    "--model",
    type=str,
    help="model class name to export",
)
def export_json(dirname: str, model: str):
    # list all model classes extending db.Model
    db_model_classes = [obj for name, obj in list_db_models()]

    # filter by model name if provided
    if model:
        db_model_classes = [obj for obj in db_model_classes if obj.__name__ == model]

    for db_model_class in db_model_classes:
        obj_list = []
        model_name = db_model_class.__name__.lower()

        for obj in db_model_class.query.all():
            obj_list.append(obj.json.get("data"))
        if obj_list:
            json_path = f"{dirname}/{model_name}.json"
            logging.info(f"Exporting {model_name} to: {json_path}")
            with open(json_path, "w") as f:
                json.dump(obj_list, f, indent=4)
                logging.info(f"Exported {model_name}.")
        else:
            logging.info(f"Could not find any {model_name} objects to export.")
