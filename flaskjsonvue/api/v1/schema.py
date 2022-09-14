import logging

from flask import Blueprint, jsonify, request
from jsonschema import FormatChecker, ValidationError, Draft202012Validator, validate

from flaskjsonvue.api.v1.schemes.demo import DemoJsonSchema

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_schema", __name__, url_prefix="/schema")

ENDPOINT_SCHEMA_MAPPING = {
    "demo": DemoJsonSchema,
}


def get_schema_from_url(url):
    endpoint = url.split(bp.url_prefix)[0].split("/")[-1]
    return ENDPOINT_SCHEMA_MAPPING[endpoint]


def validate_json_request(request, json_schema):
    """
    Verify that request is a json request and validate the given schema
    Return list of errors
    :param request: flask request
    :param json_schema: json schema to apply
    """
    errors = []
    if not request.is_json:
        errors.append({"Request": "Only json requests are accepted!"})
        return errors

    try:
        validate(
            instance=request.json,
            schema=json_schema,
            format_checker=FormatChecker(),
        )
    except ValidationError as e:
        v = Draft202012Validator(json_schema, format_checker=FormatChecker())
        errors = [
            {"field": error.path.pop(), "message": error.message}
            for error in v.iter_errors(request.json)
        ]

    return errors


@bp.route("/detail.schema.json", methods=("GET",))
def detail_json_schema():
    return jsonify(get_schema_from_url(request.path).detail())


@bp.route("/create.schema.json", methods=("GET",))
def create_json_schema():
    return jsonify(get_schema_from_url(request.path).create())


@bp.route("/update.schema.json", methods=("GET",))
def update_json_schema():
    return jsonify(get_schema_from_url(request.path).update())


@bp.route("/delete.schema.json", methods=("GET",))
def delete_json_schema():
    return jsonify(get_schema_from_url(request.path).delete())


@bp.route("/array.schema.json", methods=("GET",))
def array_json_schema():
    return jsonify(get_schema_from_url(request.path).array())
