from flask import Blueprint, jsonify
from flask_login import login_required
from olapy.core.mdx.executor.execute import MdxEngine
API = Blueprint('api', __name__, template_folder='templates')
api = API.route


@api('/cubes')
@login_required
def get_cubes():
    executor = MdxEngine()
    data = executor.get_cubes_names()
    return jsonify(data)

@api('/cubes/dimensions/<cube_name>')
@login_required
def get_cube_dimensions(cube_name):
    executor = MdxEngine()
    executor.load_cube(cube_name)
    data = executor.tables_loaded.keys()
    return jsonify(data)