import logging
import inspect

from flask import Blueprint, jsonify
from flaskjsonvue import models
from flaskjsonvue.db import db

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("api_endpoints", __name__, url_prefix="/api/v1/endpoints")


@bp.route("/", methods=("GET",))
def index():
    #  return list of all member names members that extend db.Model
    obj_list = [
        name.lower()
        for name, obj in inspect.getmembers(models)
        if hasattr(obj, "__mro__") and db.Model in obj.__mro__
    ]

    return jsonify(obj_list)
