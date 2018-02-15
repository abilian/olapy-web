import shutil
from distutils.dir_util import copy_tree
from os.path import expanduser, isdir

import os
from flask import Blueprint, jsonify
from flask_login import login_required
from olapy.core.mdx.executor.execute import MdxEngine
from olapy.core.mdx.tools.config_file_parser import ConfigParser
from olapy.core.mdx.tools.olapy_config_file_parser import DbConfigParser
from flask import request
from werkzeug.utils import secure_filename
import pandas as pd

API = Blueprint('api', __name__, template_folder='templates')
api = API.route

ALLOWED_EXTENSIONS = {'csv'}
# todo remove
TEMP_CUBE_NAME = 'TEMP'
TEMP_OLAPY_DIR = '/home/moddoy/PycharmProjects/olapy-web/instance/olapy-data'

home = expanduser('~')
# todo all this will be repalced with db
OLAPY_DATA_SOURCE = ('csv')
# OLAPY_DB_CONFIG_FILE_PATH = os.path.join(home, 'olapy-data', 'olapy-config.yml')
OLAPY_CUBE_CONFIG_FILE = os.path.join(home, 'olapy-data', 'cubes', 'cubes-config.yml')


def get_olapy_config(source_type, db_config_file, cube_config_file):
    db_conf = None
    cube_conf = None

    if 'db' in source_type:
        db_config = DbConfigParser()
        db_conf = db_config.get_db_credentials(db_config_file)

    try:
        cube_config_file_parser = ConfigParser()
        cube_conf = cube_config_file_parser.get_cube_config(cube_config_file)
    except (KeyError, IOError):
        db_conf = None
    return {'db_config': db_conf,
            'cube_config': cube_conf}


@api('/cubes')
@login_required
def get_cubes():
    # conf = None
    # return {'db_config': db_conf,
    #         'cube_config': cube_conf}
    config = get_olapy_config(OLAPY_DATA_SOURCE, db_config_file=None, cube_config_file=OLAPY_CUBE_CONFIG_FILE)
    executor = MdxEngine(source_type=OLAPY_DATA_SOURCE, cube_config=config['cube_config'])
    data = executor.get_cubes_names()
    return jsonify(data)


@api('/cubes/dimensions/<cube_name>')
@login_required
def get_cube_dimensions(cube_name):
    config = get_olapy_config(OLAPY_DATA_SOURCE, db_config_file=None, cube_config_file=OLAPY_CUBE_CONFIG_FILE)
    executor = MdxEngine(source_type=OLAPY_DATA_SOURCE, cube_config=config['cube_config'])
    executor.load_cube(cube_name)
    data = executor.get_all_tables_names(ignore_fact=True)
    return jsonify(data)


@api('/cubes/facts/<cube_name>')
@login_required
def get_cube_facts(cube_name):
    config = get_olapy_config(OLAPY_DATA_SOURCE, db_config_file=None, cube_config_file=OLAPY_CUBE_CONFIG_FILE)
    executor = MdxEngine(source_type=OLAPY_DATA_SOURCE, cube_config=config['cube_config'])
    executor.load_cube(cube_name)
    data = {'table_name':
                executor.facts,
            'measures':
                executor.measures
            }
    return jsonify(data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clean_temp_dir(olapy_data_dir):
    for the_file in os.listdir(olapy_data_dir):
        file_path = os.path.join(olapy_data_dir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def try_construct_cube(cube_path):
    executor = MdxEngine(source_type='csv', cubes_path=cube_path)
    # try to construct automatically the cube
    try:
        executor.load_cube(TEMP_CUBE_NAME)
        return {
            'dimensions': executor.get_all_tables_names(ignore_fact=True),
            'facts': executor.facts,
            'measures': executor.measures
        }
    except:
        return {}


@api('/cubes/add', methods=['POST'])
@login_required
def add_cube():
    # temporary
    clean_temp_dir(os.path.join(TEMP_OLAPY_DIR, TEMP_CUBE_NAME))
    if request.method == 'POST':
        all_file = request.files.getlist('files')
        for file_uploaded in all_file:
            if file_uploaded and allowed_file(file_uploaded.filename):
                filename = secure_filename(file_uploaded.filename)
                file_uploaded.save(os.path.join(TEMP_OLAPY_DIR, TEMP_CUBE_NAME, filename))

        construction = try_construct_cube(TEMP_OLAPY_DIR)
        if construction:
            return jsonify(construction)
        else:
            return jsonify(
                {'facts': None,
                 'dimensions': [file.filename for file in all_file],
                 'measures': None
                 }
            )


@api('/cubes/confirm_cube', methods=['POST'])
@login_required
def confirm_cube():
    temp_dir = os.path.join(TEMP_OLAPY_DIR, TEMP_CUBE_NAME)
    if request.data and request.method == 'POST':
        if isdir(temp_dir):
            # todo temp to fix
            copy_tree(temp_dir, os.path.join(TEMP_OLAPY_DIR, 'cubes', request.data))
            shutil.rmtree(temp_dir)
            return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/get_table_columns_no_id', methods=['POST'])
@login_required
def get_table_columns_no_id():
    temp_dir = os.path.join(TEMP_OLAPY_DIR, TEMP_CUBE_NAME)
    if request.data and request.method == 'POST':
        if isdir(temp_dir):
            df = pd.read_csv(os.path.join(temp_dir, request.data), sep=';')
            # todo show columns with there types
            # df.dtypes.to_dict()
            return jsonify(
                [column for column in df.columns if '_id' not in column.lower()[-3:] and 'id' != column.lower()])
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/get_tables_and_columns', methods=['POST'])
@login_required
def get_tables_and_columns():
    temp_dir = os.path.join(TEMP_OLAPY_DIR, TEMP_CUBE_NAME)
    if request.data and request.method == 'POST':
        if isdir(temp_dir):
            response = {}
            print(request.data)
            att_tables = request.data.split(',')
            print(att_tables)
            print(type(att_tables))
            for table_name in att_tables:
                print(table_name)
                df = pd.read_csv(os.path.join(temp_dir, table_name), sep=';')
                response[table_name] = list(df.columns)
            return jsonify(response)
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}
