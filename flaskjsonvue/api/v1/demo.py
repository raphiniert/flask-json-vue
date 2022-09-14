import logging

from flask import Blueprint, jsonify, request
from flaskjsonvue.db import db
from flaskjsonvue.models import Demo
from flaskjsonvue.api.v1.schemes.demo import DemoJsonSchema
from flaskjsonvue.api.v1.schema import bp as api_v1_schema
from flaskjsonvue.api.v1.schema import validate_json_request

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_demo", __name__, url_prefix="/api/v1/demo")
bp.register_blueprint(api_v1_schema)
logger.info("Registered nested api_v1_schema blueprint for api_v1_demo blueprint.")


@bp.route("/list", methods=("GET",))
def list():
    obj_list = []
    for obj in Demo.query.all():
        obj_list.append(obj.json)
    return jsonify(obj_list)


@bp.route("/add", methods=("POST",))
def create():
    response = {
        "messages": [],
        "infos": [],
        "warnings": [],
        "errors": validate_json_request(
            request=request, json_schema=DemoJsonSchema.create()
        ),
        "objects": [],
    }
    if len(response["errors"]):
        logger.error(f"Data not valid! Errors: {response['errors']}")
        response["status"] = "failure"
        response["errors"].append(response["errors"])
        return jsonify(response), 400

    # no errors, data is valid
    valid_data = request.json

    # create object
    obj = Demo(**valid_data)
    db.session.add(obj)
    db.session.commit()
    logger.info(f"Created new: {obj}")

    response["infos"].append(
        f"Created new {DemoJsonSchema.name.lower()} with id: {obj.id}"
    )
    response["objects"].append(obj.json)
    return jsonify(response), 201
