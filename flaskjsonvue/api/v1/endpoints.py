import logging

from flask import Blueprint, jsonify
from flaskjsonvue.db import list_db_models

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_endpoints", __name__, url_prefix="/api/v1/endpoints")


@bp.route("/", methods=("GET",))
def index():
    obj_list = [name.lower() for name, obj in list_db_models()]

    return jsonify(obj_list)
