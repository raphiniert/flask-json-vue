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
        "infos": [],
        "success": [],
        "warnings": [],
        "errors": validate_json_request(
            request=request, json_schema=DemoJsonSchema.create()
        ),
        "objects": [],
    }
    if len(response["errors"]):
        logger.error(f"Data not valid! Errors: {response['errors']}")
        return jsonify(response), 400

    # no errors, data is valid
    valid_data = request.json

    # create object
    obj = Demo(**valid_data)
    db.session.add(obj)
    db.session.commit()
    logger.info(f"Created new: {obj}")

    response["success"].append(
        f"Created new {DemoJsonSchema.name.lower()} with id: {obj.id}"
    )
    response["objects"].append(obj.json)
    return jsonify(response), 201


@bp.route("/get/<int:obj_id>", methods=("GET",))
def get(obj_id):
    response = {
        "infos": [],
        "success": [],
        "warnings": [],
        "errors": [],
        "objects": [],
    }
    obj = Demo.query.get(obj_id)
    if obj:
        response["objects"].append(obj.json)
        return jsonify(response), 200

    response["errors"].append(
        {"object_id": f"No {DemoJsonSchema.name.lower()} with id: {obj_id} available"}
    )
    return jsonify(response), 404


@bp.route("/update", methods=("PATCH",))
def update():
    response = {
        "infos": [],
        "success": [],
        "warnings": [],
        "errors": validate_json_request(
            request=request, json_schema=DemoJsonSchema.update()
        ),
        "objects": [],
    }
    if len(response["errors"]):
        logger.error(f"Data not valid! Errors: {response['errors']}")
        return jsonify(response), 400

    # no errors, data is valid
    valid_data = request.json

    obj = Demo.query.get(valid_data["id"])
    if obj:
        obj.update(**valid_data)
        db.session.add(obj)
        db.session.commit()
        logger.info(f"Updated {obj}")

        response["success"].append(
            f"Updated {DemoJsonSchema.name.lower()} with id: {obj.id}"
        )
        response["objects"].append(obj.json)
        return jsonify(response), 200

    response["errors"].append(
        {
            "object_id": f"No {DemoJsonSchema.name.lower()} with id: {valid_data['id']} available"
        }
    )
    return jsonify(response), 404


@bp.route("/delete", methods=("DELETE",))
def delete():
    response = {
        "infos": [],
        "success": [],
        "warnings": [],
        "errors": validate_json_request(
            request=request, json_schema=DemoJsonSchema.delete()
        ),
        "objects": [],
    }
    if len(response["errors"]):
        logger.error(f"Data not valid! Errors: {response['errors']}")
        return jsonify(response), 400

    # no errors, data is valid
    valid_data = request.json

    obj = Demo.query.get(valid_data["id"])
    if obj:
        db.session.delete(obj)
        db.session.commit()
        logger.info(f"Deleted {obj}")
        response["success"].append(
            f"Deleted {DemoJsonSchema.name.lower()} with id: {obj.id}"
        )
        return jsonify(response), 200

    response["errors"].append(
        {
            "object_id": f"No {DemoJsonSchema.name.lower()} with id: {valid_data['id']} available"
        }
    )
    return jsonify(response), 400
