import logging

from flask import Blueprint, render_template

logger = logging.getLogger("flaskjsonvue")

bp = Blueprint("demo", __name__)


@bp.route("/", methods=("GET",))
def index():
    return render_template(f"base.html")
