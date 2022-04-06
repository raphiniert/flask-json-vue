import logging

from flask import Blueprint, jsonify
from flaskjsonvue.models import Demo

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_demo", __name__, url_prefix="/api/v1/demo")


@bp.route("/list", methods=("GET",))
def list():
    obj_list = []
    for obj in Demo.query.all():
        obj_list.append(obj.json)
    return jsonify(obj_list)
