# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import shutil
import tempfile
from collections import OrderedDict
from distutils.dir_util import copy_tree
from os.path import expanduser, isdir
from six.moves.urllib.parse import urlunparse

import os

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from olapy.core.mdx.executor.execute import MdxEngine
from flask import request
from pathlib import Path
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import pandas as pd
import json
from flask import current_app

from app.extensions import db
from app.models import Cube, User, Dashboard

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


@api('cubes')
@login_required
def get_cubes():
    user_cubes = User.query.filter(User.id == current_user.id).first().cubes.all()
    return jsonify([cube.name for cube in user_cubes])


def _load_cube(cube_name):
    config = get_config(cube_name)
    source_type = get_cube_source_type(cube_name)
    if config['db_config']:
        sqla_engine = create_engine(config['db_config'])
    else:
        sqla_engine = None
    olapy_data_location = os.path.join(current_app.instance_path, 'olapy-data')
    executor = MdxEngine(source_type=source_type, sqla_engine=sqla_engine,
                         cube_config=config['cube_config'], olapy_data_location=olapy_data_location)
    executor.load_cube(cube_name)
    return executor


@api('cubes/<cube_name>/dimensions')
@login_required
def get_cube_dimensions(cube_name):
    executor = _load_cube(cube_name)
    tables_names = executor.get_all_tables_names(ignore_fact=True)
    return jsonify(tables_names)


@api('cubes/<cube_name>/facts')
@login_required
def get_cube_facts(cube_name):
    cube = _load_cube(cube_name)
    cube_info = {
        'table_name': cube.facts,
        'measures': cube.measures
    }
    return jsonify(cube_info)


def allowed_file(filename):
    file_extension = Path(filename).suffix
    return file_extension in ALLOWED_EXTENSIONS


def clean_temp_dir(olapy_data_dir):
    for the_file in os.listdir(olapy_data_dir):
        file_path = os.path.join(olapy_data_dir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def construct_cube(cube_name, sqla_engine=None, source_type='csv', olapy_data_location=None):
    executor = MdxEngine(sqla_engine=sqla_engine, source_type=source_type,
                         olapy_data_location=olapy_data_location, cubes_folder=TEMP_CUBE_NAME)
    # try to construct automatically the cube
    try:
        temp_cube_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME)
        executor.load_cube(cube_name, cube_folder=temp_cube_path)
        return {
            'dimensions': executor.get_all_tables_names(ignore_fact=True),
            'facts': executor.facts,
            'measures': executor.measures
        }
    except:
        return {
            'all_tables': executor.get_all_tables_names(ignore_fact=False),
        }


@api('cubes/add', methods=['POST'])
@login_required
def add_cube():
    # temporary
    #  2 TEMP_CUBE_NAME = first is the all cubes folder, the second is the current cube folder
    cube_dir = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME)
    if isdir(cube_dir):
        clean_temp_dir(cube_dir)
    else:
        os.makedirs(cube_dir)
    all_file = request.files.getlist('files')
    for file_uploaded in all_file:
        if file_uploaded and allowed_file(file_uploaded.filename):
            filename = secure_filename(file_uploaded.filename)
            file_uploaded.save(os.path.join(cube_dir, filename))
    cube = construct_cube(cube_name=TEMP_CUBE_NAME, olapy_data_location=OLAPY_TEMP_DIR, source_type='csv')
    if 'dimensions' in cube:
        return jsonify(cube)
    else:
        return jsonify(
            {'facts': None,
             'dimensions': [file.filename for file in all_file],
             'measures': None
             }
        )


@api('cubes/confirm_cube', methods=['POST'])
@login_required
def confirm_cube():
    if request.data:
        request_data = json.loads(request.data)
        custom_cube = request_data['customCube']
        cube_name = request_data['cubeName'].decode('utf-8')
        if custom_cube:
            temp_folder = cube_name
        else:
            temp_folder = TEMP_CUBE_NAME
            save_cube_config_2_db(config=None, cube_name=cube_name, source='csv')
        new_temp_dir = os.path.join(OLAPY_TEMP_DIR, temp_folder)
        if isdir(new_temp_dir):
            olapy_data_dir = os.path.join(current_app.instance_path, 'olapy-data', 'cubes', cube_name)
            copy_tree(new_temp_dir, olapy_data_dir)
            shutil.rmtree(new_temp_dir)
            # custom -> config with config file , no need to return response, instead wait to use the cube conf
        return jsonify({'success': True}), 200


@api('cubes/clean_tmp_dir', methods=['POST'])
@login_required
def clean_tmp_dir():
    for root, dirs, files in os.walk(OLAPY_TEMP_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return jsonify({'success': True}), 200


def get_columns_from_files(db_cube_config):
    if isdir(OLAPY_TEMP_DIR):
        cube_file_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME, db_cube_config['tableName'].decode('utf-8'))
        df = pd.read_csv(cube_file_path, sep=';')
        # todo show columns with there types
        if db_cube_config['WithID']:
            result = [column for column in df.columns]
        else:
            result = [column for column in df.columns if
                      '_id' not in column.lower()[-3:] and 'id' != column.lower()]
        return result


def get_columns_from_db(db_cube_config):
    sqla_uri = generate_sqla_uri(db_cube_config['dbConfig'])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(sqla_engine=sqla_engine, source_type='db')
    results = executor.sqla_engine.execution_options(
        stream_results=True,
    ).execute('SELECT * FROM {}'.format(db_cube_config['tableName']))
    df = pd.DataFrame(iter(results), columns=results.keys())
    if db_cube_config['WithID']:
        result = [column for column in df.columns]
    else:
        result = [column for column in df.columns if '_id' not in column.lower()[-3:] and 'id' != column.lower()]
    return result


@api('cubes/get_table_columns', methods=['POST'])
@login_required
def get_table_columns():
    db_cube_config = request.get_json()
    if db_cube_config:
        if db_cube_config['dbConfig']:
            return jsonify(get_columns_from_db(db_cube_config))
        else:
            return jsonify(get_columns_from_files(db_cube_config))
    raise Exception('cube config is not specified')


def get_tables_columns_from_db(db_cube_config):
    response = {}
    sqla_uri = generate_sqla_uri(db_cube_config['dbConfig'])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(sqla_engine=sqla_engine, source_type='db')
    att_tables = db_cube_config['allTables'].split(',')
    for table_name in att_tables:
        results = executor.sqla_engine.execution_options(stream_results=True).execute(
            'SELECT * FROM {}'.format(table_name))
        df = pd.DataFrame(iter(results), columns=results.keys())
        response[table_name] = list(df.columns)
    return response


def get_tables_columns_from_files(db_cube_config):
    if isdir(OLAPY_TEMP_DIR):
        response = {}
        att_tables = db_cube_config['allTables'].split(',')
        for table_name in att_tables:
            file_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME, table_name)
            df = pd.read_csv(file_path, sep=';')
            response[table_name] = list(df.columns)
        return response


@api('cubes/get_tables_and_columns', methods=['POST'])
@login_required
def get_tables_and_columns():
    if request.data:
        db_cube_config = json.loads(request.data.decode('utf-8'))
        if db_cube_config['dbConfig']:
            return jsonify(get_tables_columns_from_db(db_cube_config))
        else:
            return jsonify(get_tables_columns_from_files(db_cube_config))
    raise Exception('cube config is not specified')


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


def save_cube_config_2_db(config, cube_name, source):
    queried_cube = User.query.filter(User.id == current_user.id).first().cubes.filter(
        Cube.name == cube_name).first()
    # config can be None
    cube_config = config.get('cube_config') if config else None
    db_config = config.get('db_config') if config else None
    if queried_cube:
        # update cube
        queried_cube.name = cube_name
        queried_cube.source = source
        queried_cube.config = cube_config
        queried_cube.db_config = db_config
    else:
        # add new cube
        cube = Cube(users=[current_user],
                    name=cube_name,
                    source=source,
                    config=cube_config,
                    db_config=db_config
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
    db_config = generate_sqla_uri(data_request.get('dbConfig'))
    return {'cube_config': cube_conf,
            'db_config': db_config}


def construct_custom_files_cube(data_request):
    os.rename(os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME),
              os.path.join(OLAPY_TEMP_DIR, data_request['cubeName']))
    cube_config = gen_cube_conf(data_request=data_request, cube_name=data_request['cubeName'])
    executor = MdxEngine(cube_config=cube_config['cube_config'], olapy_data_location=OLAPY_TEMP_DIR)
    try:
        temp_cube_path = os.path.join(OLAPY_TEMP_DIR, data_request['cubeName'])
        executor.load_cube(data_request['cubeName'], cube_folder=temp_cube_path)
        if executor.star_schema_dataframe.columns is not None:
            save_cube_config_2_db(cube_config, data_request['cubeName'], source='csv')
            return executor.star_schema_dataframe.fillna('').head().to_html(classes=[
                'table-bordered table-striped'
            ], index=False)
    except:
        os.rename(os.path.join(OLAPY_TEMP_DIR, data_request['cubeName']),
                  os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME))
        return None


def construct_custom_db_cube(data_request):
    config = gen_cube_conf(data_request, source='db', cube_name=data_request['dbConfig']['selectCube'])
    source_type = 'db'
    sqla_uri = generate_sqla_uri(data_request['dbConfig'])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(source_type=source_type, sqla_engine=sqla_engine,
                         cube_config=config['cube_config'])
    try:
        executor.load_cube(data_request['dbConfig']['selectCube'])
        if executor.star_schema_dataframe.columns is not None:
            save_cube_config_2_db(config, data_request['dbConfig']['selectCube'], source='db')
            return executor.star_schema_dataframe.fillna('').head().to_html(classes=[
                'table-bordered table-striped'
            ], index=False)
    except:
        return None


@api('cubes/try_construct_custom_cube', methods=['POST'])
@login_required
def construct_custom_cube():
    if request.data:
        data_request = json.loads(request.data)
        if data_request['dbConfig']:
            star_schema_table = construct_custom_db_cube(data_request)
        else:
            star_schema_table = construct_custom_files_cube(data_request)
        if star_schema_table:
            return jsonify(star_schema_table)
        else:
            raise Exception('unable to construct cube')


def generate_sqla_uri(db_credentials):
    engine = db_credentials['engine'].lower().replace('postgres', 'postgresql')
    user = db_credentials['username']
    password = db_credentials['password']
    server = db_credentials['servername']
    port = db_credentials['port']
    # todo change
    # return urlunparse((engine, user, password, "", "", "")) + '@' + server + ':' + port
    if 'selectCube' in db_credentials:
        selected_db = '/' + db_credentials['selectCube']
    else:
        selected_db = ''

    return engine + '://' + user + ':' + password + '@' + server + ':' + port + selected_db


@api('cubes/connectDB', methods=['POST'])
@login_required
def connectDB():
    if request.data:
        sqla_uri = generate_sqla_uri(json.loads(request.data))
        sqla_engine = create_engine(sqla_uri)
        executor = MdxEngine(source_type="db", sqla_engine=sqla_engine)
        return jsonify(executor.get_cubes_names())


@api('cubes/add_DB_cube', methods=['POST'])
@login_required
def add_db_cube():
    request_data = request.get_json()
    sqla_uri = generate_sqla_uri(json.loads(request.data))
    sqla_engine = create_engine(sqla_uri)
    construction = construct_cube(cube_name=request_data['selectCube'], source_type='db',
                                  sqla_engine=sqla_engine, olapy_data_location=current_app.instance_path)
    if 'dimensions' in construction:
        return jsonify(construction)
    else:
        return jsonify(
            {'facts': None,
             'dimensions': construction['all_tables'],
             'measures': None
             }
        )


@api('cubes/confirm_db_cube', methods=['POST'])
@login_required
def confirm_db_cube():
    request_data = request.get_json()
    config = {'cube_config': None,
              'db_config': generate_sqla_uri(request_data)}
    save_cube_config_2_db(config=config, cube_name=request_data['selectCube'], source='db')
    return jsonify({'success': True}), 200


@api('cubes/chart_columns', methods=['POST'])
@login_required
def get_chart_columns_result():
    request_data = request.get_json()
    executor = _load_cube(request_data['selectedCube'])
    return executor.star_schema_dataframe.groupby([request_data['selectedColumn']]).sum()[
        request_data['selectedMeasures']].to_json()


@api('cubes/<cube_name>/columns')
@login_required
def get_cube_columns(cube_name):
    executor = _load_cube(cube_name)
    return jsonify([column for column in executor.star_schema_dataframe.columns if
                    column.lower()[-3:] != '_id' and column not in executor.measures])


@api('dashboard/save', methods=['POST'])
@login_required
def save_dashboard():
    request_data = request.get_json()
    user_dashboard = User.query.filter(User.id == current_user.id).first().dashboards
    if user_dashboard:
        # update dashboard
        user_dashboard.name = request_data['dashboardName']
        user_dashboard.content = request_data['dashboardContent']
    else:
        # add new cube
        cube = Dashboard(name=request_data['dashboardName'],
                         content=request_data['dashboardContent'],
                         user_id=current_user.id
                         )
        db.session.add(cube)
    db.session.commit()
    return jsonify({'success': True}), 200
