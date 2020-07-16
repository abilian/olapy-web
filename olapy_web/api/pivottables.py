from flask import jsonify, request

from olapy_web.extensions import db
from olapy_web.models import Cube, Pivottable, User

from . import route
from .util import get_current_user


@route("/pivottable/save", methods=["POST"])
def save_pivottable():
    request_data = request.get_json()
    user_pivottable = (
        get_current_user()
        .pivottables.filter(Pivottable.name == request_data["pivottableName"])
        .first()
    )
    selected_cube = Cube.query.filter(
        User.id == get_current_user().id, Cube.name == request_data["cubeName"]
    ).first()
    if user_pivottable:
        user_pivottable.name = request_data["pivottableName"]
        user_pivottable.rows = request_data["pvtRows"]
        user_pivottable.columns = request_data["pvtCols"]
    else:
        pivottable = Pivottable(
            user_id=get_current_user().id,
            name=request_data["pivottableName"],
            rows=request_data["pvtRows"],
            columns=request_data["pvtCols"],
            cube=selected_cube,
        )
        db.session.add(pivottable)
    db.session.commit()
    return jsonify({"success": True}), 200


@route("/pivottable/<pivottable_name>")
def get_pivottable(pivottable_name):
    pivottable = (
        get_current_user()
        .pivottables.filter(Pivottable.name == pivottable_name)
        .first()
    )
    return jsonify(
        {
            "name": pivottable.name,
            "columns": pivottable.columns,
            "rows": pivottable.rows,
            "cube_name": pivottable.cube.name,
        }
    )


@route("/pivottable/all")
def all_pivottables():
    all_pivottables = get_current_user().pivottables
    return jsonify([pivottable.name for pivottable in all_pivottables])


@route("/pivottable/delete", methods=["POST"])
def delete_pivottable():
    request_data = request.get_json()
    obj = (
        get_current_user()
        .pivottables.filter(Pivottable.name == request_data["pivottableName"])
        .first()
    )
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"success": True}), 200
