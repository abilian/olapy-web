# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import shutil
import tempfile
from collections import OrderedDict
from distutils.dir_util import copy_tree
from os.path import expanduser, isdir

import os

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from olapy.core.mdx.executor.execute import MdxEngine
from flask import request
from pathlib import Path
from werkzeug.utils import secure_filename
import pandas as pd
import json
from flask import current_app

from app.extensions import db
from app.models import Cube, User

API = Blueprint('api', __name__, template_folder='templates')
api = API.route

ALLOWED_EXTENSIONS = {'.csv'}
TEMP_CUBE_NAME = 'TEMP_CUBE'
OLAPY_TEMP_DIR = os.path.join(tempfile.mkdtemp(), 'TEMP')
home = expanduser('~')


def get_cube(cube_name):
    return User.query.filter(User.id == current_user.id).first().cubes.filter(
        Cube.name == cube_name).first()


def get_cube_source_type(cube_name):
    cube_result = get_cube(cube_name)
    return cube_result.source


def get_config(cube_name):
    cube_result = get_cube(cube_name)
    return {
        'db_config': cube_result.db_config if cube_result and cube_result.db_config else None,
        'cube_config': cube_result.config if cube_result and cube_result.config else None
    }


@api('/cubes')
@login_required
def get_cubes():
    return jsonify([cube.name for cube in Cube.query.all()])


def _load_cube(cube_name):
    config = get_config(cube_name)
    source_type = get_cube_source_type(cube_name)
    executor = MdxEngine(source_type=source_type, database_config=config['db_config'],
                         cube_config=config['cube_config'])
    executor.load_cube(cube_name)
    return executor


@api('/cubes/<cube_name>/dimensions')
@login_required
def get_cube_dimensions(cube_name):
    executor = _load_cube(cube_name)
    data = executor.get_all_tables_names(ignore_fact=True)
    return jsonify(data)


@api('/cubes/<cube_name>/facts')
@login_required
def get_cube_facts(cube_name):
    executor = _load_cube(cube_name)
    data = {
        'table_name': executor.facts,
        'measures': executor.measures
    }
    return jsonify(data)


def allowed_file(filename):
    file_extension = Path(filename).suffix
    return file_extension in ALLOWED_EXTENSIONS


def clean_temp_dir(olapy_data_dir):
    for the_file in os.listdir(olapy_data_dir):
        file_path = os.path.join(olapy_data_dir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def try_construct_cube(cube_name, **kwargs):
    database_config = kwargs.get('database_config', None)
    source_type = kwargs.get('source_type', 'csv')
    cubes_path = kwargs.get('cubes_path', None)

    executor = MdxEngine(database_config=database_config, source_type=source_type, cubes_path=cubes_path)
    # try to construct automatically the cube
    try:
        executor.load_cube(cube_name)
        return {
            'dimensions': executor.get_all_tables_names(ignore_fact=True),
            'facts': executor.facts,
            'measures': executor.measures
        }
    except:
        return {
            'all_tables': executor.get_all_tables_names(ignore_fact=False),
        }


@api('/cubes/add', methods=['POST'])
@login_required
def add_cube():
    # temporary
    cube_dir = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME)
    if isdir(cube_dir):
        clean_temp_dir(cube_dir)
    else:
        os.makedirs(cube_dir)
    if request.method == 'POST':
        all_file = request.files.getlist('files')
        for file_uploaded in all_file:
            if file_uploaded and allowed_file(file_uploaded.filename):
                filename = secure_filename(file_uploaded.filename)
                file_uploaded.save(os.path.join(cube_dir, filename))

        cube = try_construct_cube(cube_name=TEMP_CUBE_NAME, cubes_path=OLAPY_TEMP_DIR,
                                  source_type='csv')

        if 'dimensions' in cube:
            return jsonify(cube)
        else:
            return jsonify(
                {'facts': None,
                 'dimensions': [file.filename for file in all_file],
                 'measures': None
                 }
            )


@api('/cubes/confirm_cube', methods=['POST'])
@login_required
def confirm_cube(custom=False):
    if request.data and request.method == 'POST':
        if custom:
            temp_folder = request.data.decode('utf-8')
        else:
            temp_folder = TEMP_CUBE_NAME
        new_temp_dir = os.path.join(OLAPY_TEMP_DIR, temp_folder)
        if isdir(new_temp_dir):
            # todo temp to fix
            copy_tree(new_temp_dir, os.path.join(current_app.instance_path, 'olapy-data', 'cubes',
                                                 request.data.decode('utf-8')))
            shutil.rmtree(new_temp_dir)
            if not custom:
                # custom -> config with config file , no need to return response, instead wait to use the cube conf
                save_cube_config_2_db(cube_config=None, cube_name=request.data.decode('utf-8'), source='csv')
                return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/clean_tmp_dir', methods=['POST'])
@login_required
def clean_tmp_dir():
    for root, dirs, files in os.walk(OLAPY_TEMP_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


def get_columns_from_files(data):
    if isdir(OLAPY_TEMP_DIR):
        cube_file_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME, data['tableName'].decode('utf-8'))
        df = pd.read_csv(cube_file_path, sep=';')
        # todo show columns with there types
        if data['WithID']:
            result = [column for column in df.columns]
        else:
            result = [column for column in df.columns if
                      '_id' not in column.lower()[-3:] and 'id' != column.lower()]
        return jsonify(result)


def get_db_config(data_config):
    return {
        'dbms': data_config['engine'].lower(),
        'host': data_config['servername'],
        'port': data_config['port'],
        'user': data_config['username'],
        'password': data_config['password']
    }


def get_columns_from_db(data):
    config = get_db_config(data['dbConfig'])
    executor = MdxEngine(database_config=config, source_type='db')
    engine = executor.instantiate_db(data['dbConfig']['selectCube']).engine
    results = engine.execution_options(
        stream_results=True,
    ).execute('SELECT * FROM {}'.format(data['tableName']))
    df = pd.DataFrame(iter(results), columns=results.keys())
    if data['WithID']:
        result = [column for column in df.columns]
    else:
        result = [column for column in df.columns if '_id' not in column.lower()[-3:] and 'id' != column.lower()]
    return jsonify(result)


@api('/cubes/get_table_columns', methods=['POST'])
@login_required
def get_table_columns():
    data = request.get_json()
    if data and request.method == 'POST':
        if data['dbConfig']:
            return get_columns_from_db(data)
        else:
            return get_columns_from_files(data)
    return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


def get_tables_columns_from_db(data):
    response = {}
    config = get_db_config(data['dbConfig'])
    executor = MdxEngine(database_config=config, source_type='db')
    engine = executor.instantiate_db(data['dbConfig']['selectCube']).engine
    att_tables = data['allTables'].split(',')
    for table_name in att_tables:
        results = engine.execution_options(
            stream_results=True,
        ).execute('SELECT * FROM {}'.format(table_name))
        df = pd.DataFrame(iter(results), columns=results.keys())
        response[table_name] = list(df.columns)
    return jsonify(response)


def get_tables_columns_from_files(data):
    if isdir(OLAPY_TEMP_DIR):
        response = {}
        att_tables = data['allTables'].split(',')
        for table_name in att_tables:
            file_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME, table_name)
            df = pd.read_csv(file_path, sep=';')
            response[table_name] = list(df.columns)
        return jsonify(response)


@api('/cubes/get_tables_and_columns', methods=['POST'])
@login_required
def get_tables_and_columns():
    if request.data and request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        if data['dbConfig']:
            return get_tables_columns_from_db(data)
        else:
            return get_tables_columns_from_files(data)
    return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


def _gen_facts(data_request):
    """
    TEMPORARY
    :param data_request:
    :return:
    """
    columns_names = []
    refs = []
    for table in data_request['tablesAndColumnsResult']:
        columns_names.append(data_request['tablesAndColumnsResult'][table]['FactsCol'])
        refs.append(table.replace('.csv', '') + '.' + data_request['tablesAndColumnsResult'][table]['DimCol'])

    keys = dict((column, refs[index]) for (index, column) in enumerate(columns_names))
    return {
        'table_name': data_request['factsTable'].replace('.csv', ''),
        'keys': keys,
        'measures': data_request['measures']
    }


def check_specified_table_column(table_name, data_request):
    columns = OrderedDict()
    for table_col in data_request['columnsPerDimension']:
        if table_col and table_col['table'].replace('.csv', '') == table_name:
            for column in table_col['columns']:
                columns.update({column: column})
    return columns


def _gen_dimensions(data_request):
    """
    TEMPORARY
    :param data_request:
    :return:
    """
    facts_table = data_request['factsTable'].replace('.csv', '')
    dimensions = [
        {
            'name': facts_table,
            'displayName': facts_table
        }
    ]
    for table in data_request['tablesAndColumnsResult']:
        table_name = table.replace('.csv', '')
        columns = check_specified_table_column(table_name, data_request)
        dimensions.append({
            'name': table_name,
            'displayName': table_name,
            'columns': columns
        })

    return dimensions


def save_cube_config_2_db(cube_config, cube_name, source):
    queried_cube = User.query.filter(User.id == current_user.id).first().cubes.filter(
        Cube.name == cube_name).first()
    if queried_cube:
        # update cube
        queried_cube.name = cube_name
        queried_cube.source = source
        queried_cube.config = cube_config['cube_config'] if cube_config and cube_config['cube_config'] else None
        queried_cube.db_config = str(cube_config['db_config']) if cube_config and cube_config['db_config'] else None
    else:
        # add new cube
        cube = Cube(users=[current_user],
                    name=cube_name,
                    source=source,
                    config=cube_config['db_config'] if cube_config and cube_config['db_config'] else None,
                    db_config=str(cube_config['db_config']) if cube_config and cube_config['db_config'] else None
                    )
        db.session.add(cube)
    db.session.commit()


def gen_cube_conf(data_request, source='csv', cube_name=None):
    """
    Temporary function
    :return:
    """
    facts = _gen_facts(data_request)
    dimensions = _gen_dimensions(data_request)
    cube_conf = {
        'name': data_request['cubeName'] if not cube_name else cube_name,
        'source': source,
        'xmla_authentication': False,
        'facts': facts,
        'dimensions': dimensions
    }
    db_config = data_request['dbConfig'] if 'dbConfig' in data_request else None
    return {'cube_config': cube_conf,
            'db_config': db_config}


def try_construct_custom_files_cube(data_request):
    os.rename(os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME),
              os.path.join(OLAPY_TEMP_DIR, data_request['cubeName']))
    cube_config = gen_cube_conf(data_request=data_request, cube_name=data_request['cubeName'])
    executor = MdxEngine(cube_config=cube_config['cube_config'], cubes_path=OLAPY_TEMP_DIR)
    try:
        executor.load_cube(data_request['cubeName'])
        if executor.star_schema_dataframe.columns is not None:
            save_cube_config_2_db(cube_config, data_request['cubeName'], source='csv')
            return jsonify(executor.star_schema_dataframe.fillna('').head().to_html(classes=[
                'table-bordered table-striped'
            ], index=False))
    except:
        os.rename(os.path.join(OLAPY_TEMP_DIR, data_request['cubeName']),
                  os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME))
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


def try_construct_custom_db_cube(data_request):
    config = gen_cube_conf(data_request, source='db', cube_name=data_request['dbConfig']['selectCube'])
    source_type = 'db'
    db_config = get_db_config(data_request['dbConfig'])
    executor = MdxEngine(source_type=source_type, database_config=db_config,
                         cube_config=config['cube_config'])
    try:
        executor.load_cube(data_request['dbConfig']['selectCube'])
        if executor.star_schema_dataframe.columns is not None:
            save_cube_config_2_db(config, data_request['dbConfig']['selectCube'], source='db')
            return jsonify(executor.star_schema_dataframe.fillna('').head().to_html(classes=[
                'table-bordered table-striped'
            ], index=False))
    except:
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/try_construct_custom_cube', methods=['POST'])
@login_required
def try_construct_custom_cube():
    if request.data and request.method == 'POST':
        data_request = json.loads(request.data)
        if data_request['dbConfig']:
            return try_construct_custom_db_cube(data_request)
        else:
            return try_construct_custom_files_cube(data_request)


@api('/cubes/confirm_custom_cube', methods=['POST'])
@login_required
def confirm_custom_cube():
    try:
        confirm_cube(custom=True)
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
    except:
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/connectDB', methods=['POST'])
@login_required
def connectDB():
    if request.data and request.method == 'POST':
        data_request = json.loads(request.data)
        data_connection = get_db_config(data_request)
        executor = MdxEngine(source_type="db", database_config=data_connection)
        return jsonify(executor.get_cubes_names())


@api('/cubes/add_DB_cube', methods=['POST'])
@login_required
def add_db_cube():
    if request.method == 'POST':
        data = request.get_json()
        db_credentials = get_db_config(data)
        construction = try_construct_cube(cube_name=data['selectCube'], source_type='db', facts='facts',
                                          database_config=db_credentials)
        if 'dimensions' in construction:
            return jsonify(construction)
        else:
            return jsonify(
                {'facts': None,
                 'dimensions': construction['all_tables'],
                 'measures': None
                 }
            )


@api('/cubes/confirm_db_cube', methods=['POST'])
@login_required
def confirm_db_cube():
    if request.method == 'POST':
        data = request.get_json()
        config = {'cube_config': get_db_config(data),
                  'db_config': None}
        save_cube_config_2_db(cube_config=config, cube_name=data['selectCube'], source='db')
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
