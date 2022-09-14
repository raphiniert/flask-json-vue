import logging

from flask import Blueprint, jsonify
from flaskjsonvue.models import Demo
from flaskjsonvue.api.v1.schemes.demo import DemoJsonSchema
from flaskjsonvue.api.v1.schema import bp as schema_bp

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_demo", __name__, url_prefix="/api/v1/demo")
bp.register_blueprint(schema_bp)
logger.info("Registered schema blueprint for demo endpoint.")


@bp.route("/list", methods=("GET",))
def list():
    obj_list = []
    for obj in Demo.query.all():
        obj_list.append(obj.json)
    return jsonify(obj_list)
