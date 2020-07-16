from flask import Blueprint

api = Blueprint("api", __name__)
route = api.route


@api.record
def configure(state):
    from . import cubes, dashboards, pivottables
