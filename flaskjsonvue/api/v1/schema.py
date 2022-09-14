import logging

from flask import Blueprint, jsonify, request

from flaskjsonvue.api.v1.schemes.demo import DemoJsonSchema

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_schema", __name__, url_prefix="/schema")

ENDPOINT_SCHEMA_MAPPING = {
    "demo": DemoJsonSchema,
}


def get_schema_from_url(url):
    endpoint = url.split(bp.url_prefix)[0].split("/")[-1]
    return ENDPOINT_SCHEMA_MAPPING[endpoint]


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
