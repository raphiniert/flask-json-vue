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
