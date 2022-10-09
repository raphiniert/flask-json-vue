import logging

from flask import Blueprint, render_template

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("demo", __name__, url_prefix="/demo")


@bp.route("/", methods=("GET",))
def index():
    return render_template(f"list.html", obj_type=bp.name)


@bp.route("/add", methods=("GET",))
def create():
    return render_template(f"detail.html", obj_type=bp.name)


@bp.route("/update/<int:obj_id>", methods=("GET",))
def update(obj_id):
    return render_template(f"detail.html", obj_type=bp.name, obj_id=obj_id)
