# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import ast
import shutil
from distutils.dir_util import copy_tree
from os.path import expanduser, isdir

import os

import yaml
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from olapy.core.mdx.executor.execute import MdxEngine
from olapy.core.mdx.tools.config_file_parser import ConfigParser
from olapy.core.mdx.tools.olapy_config_file_parser import DbConfigParser
from flask import request
from werkzeug.utils import secure_filename
import pandas as pd
import json

from app.extensions import db
from app.models import Cube, User

API = Blueprint('api', __name__, template_folder='templates')
api = API.route

ALLOWED_EXTENSIONS = {'csv'}
# todo remove
# TODO REMOVE ALL TEMP TEMP TEMP
# TODO REMOVE ALL TEMP TEMP TEMP
# TODO REMOVE ALL TEMP TEMP TEMP
TEMP_CUBE_NAME = 'TEMP_CUBE'
TEMP_OLAPY_DIR = '/home/moddoy/PycharmProjects/olapy-web/instance/olapy-data'
TEMP_DIR = os.path.join(TEMP_OLAPY_DIR, 'TEMP', TEMP_CUBE_NAME)

home = expanduser('~')
# todo all this will be repalced with db
OLAPY_DATA_SOURCE = ('csv')
OLAPY_CUBE_CONFIG_FILE = '/home/moddoy/PycharmProjects/olapy-web/instance/olapy-data/cubes/cubes-config.yml'


def get_cube(cube_name):
    return User.query.filter(User.id == current_user.id).first().cubes.filter(
        Cube.name == cube_name).first()


def get_cube_source_type(cube_name):
    cube_result = get_cube(cube_name)
    return cube_result.source


def get_config(cube_name):
    # db_conf = None
    # cube_conf = None
    cube_result = get_cube(cube_name)
    # if 'db' in source_type:
    #     db_config = DbConfigParser()
    #     db_conf = db_config.get_db_credentials(db_config_file)
    #
    # try:
    #     cube_config_file_parser = ConfigParser()
    #     cube_conf = cube_config_file_parser.get_cube_config(cube_config_file)
    # except (KeyError, IOError):
    #     db_conf = None
    # print('////////////////////////////////////////////')
    # print(json.loads(cube_result.db_config.replace("'", '"')))
    if cube_result.db_config:
        db_conf = get_db_config(ast.literal_eval(cube_result.db_config))
    else:
        db_conf = None
    if cube_result.config:
        cube_config = ast.literal_eval(cube_result.config)
    else:
        cube_config = None

    return {'db_config': db_conf,
            'cube_config': cube_config
            }


@api('/cubes')
@login_required
def get_cubes():
    # cubes_path = TEMP_OLAPY_DIR + '/cubes'
    # config = get_olapy_config(OLAPY_DATA_SOURCE, db_config_file=None, cube_config_file=OLAPY_CUBE_CONFIG_FILE)
    # executor = MdxEngine(source_type=OLAPY_DATA_SOURCE, cube_config=config['cube_config'], cubes_path=cubes_path)
    # data = executor.get_cubes_names()
    return jsonify([cube.name for cube in Cube.query.all()])
    # return jsonify(data)


@api('/cubes/dimensions/<cube_name>')
@login_required
def get_cube_dimensions(cube_name):
    # config = get_olapy_config(OLAPY_DATA_SOURCE, db_config_file=None, cube_config_file=OLAPY_CUBE_CONFIG_FILE)
    config = get_config(cube_name)
    source_type = get_cube_source_type(cube_name)
    executor = MdxEngine(source_type=source_type, database_config=config['db_config'],
                         cube_config=config['cube_config'])
    executor.load_cube(cube_name)
    data = executor.get_all_tables_names(ignore_fact=True)
    return jsonify(data)


@api('/cubes/facts/<cube_name>')
@login_required
def get_cube_facts(cube_name):
    config = get_config(cube_name)
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


def try_construct_cube(cube_name, facts='Facts', **kwargs):
    database_config = kwargs.get('database_config', None)
    source_type = kwargs.get('source_type', 'csv')
    cubes_path = kwargs.get('cubes_path', None)

    executor = MdxEngine(database_config=database_config, source_type=source_type, cubes_path=cubes_path)
    # try to construct automatically the cube
    try:
        executor.load_cube(cube_name, fact_table_name=facts)
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
    if isdir(TEMP_DIR):
        clean_temp_dir(TEMP_DIR)
    else:
        os.makedirs(TEMP_DIR)
    if request.method == 'POST':
        all_file = request.files.getlist('files')
        for file_uploaded in all_file:
            if file_uploaded and allowed_file(file_uploaded.filename):
                filename = secure_filename(file_uploaded.filename)
                file_uploaded.save(os.path.join(TEMP_OLAPY_DIR, "TEMP", TEMP_CUBE_NAME, filename))

        cube = try_construct_cube(cube_name=TEMP_CUBE_NAME, cubes_path=os.path.join(TEMP_OLAPY_DIR, "TEMP"),
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
            temp_folder = 'TEMP_CUBE'
        new_temp_dir = os.path.join(TEMP_OLAPY_DIR, 'TEMP', temp_folder)
        if isdir(new_temp_dir):
            # todo temp to fix
            copy_tree(new_temp_dir, os.path.join(TEMP_OLAPY_DIR, 'cubes', request.data.decode('utf-8')))
            shutil.rmtree(new_temp_dir)
            if not custom:
                # custom -> config with config file , no need to return response, instead wait to use the cube conf
                save_2_db(cube_name=request.data.decode('utf-8'), source='csv', cube_conf=None, dbConfig=None)
                return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/clean_tmp_dir', methods=['POST'])
@login_required
def clean_tmp_dir():
    for root, dirs, files in os.walk(os.path.join(TEMP_OLAPY_DIR, 'TEMP')):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


def get_columns_from_files(data):
    if isdir(TEMP_DIR):
        df = pd.read_csv(os.path.join(TEMP_DIR, data['tableName'].decode('utf-8')), sep=';')
        # todo show columns with there types
        # df.dtypes.to_dict()
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
    if isdir(TEMP_DIR):
        response = {}
        att_tables = data['allTables'].split(',')
        for table_name in att_tables:
            df = pd.read_csv(os.path.join(TEMP_DIR, table_name), sep=';')
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
    # return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

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

    keys = {
        'columns_names': columns_names,
        'refs': refs
    }
    return {
        'table_name': data_request['factsTable'].replace('.csv', ''),
        'keys': keys,
        'measures': data_request['measures']
    }


def check_specified_table_column(table_name, data_request):
    columns = []
    for table_col in data_request['columnsPerDimension']:
        if table_col and table_col['table'].replace('.csv', '') == table_name:
            for column in table_col['columns']:
                columns.append({'name': column})
    return columns


def _gen_dimensions(data_request):
    """
    TEMPORARY
    :param data_request:
    :return:
    """
    dimensions = [
        {
            'name': data_request['factsTable'].replace('.csv', ''),
            'displayName': data_request['factsTable'].replace('.csv', '')
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


def save_2_db(cube_name, source, cube_conf, dbConfig):
    # todo teeeempp
    queried_cube = User.query.filter(User.id == current_user.id).first().cubes.filter(
        Cube.name == cube_name).first()
    if queried_cube:
        queried_cube.name = cube_name
        queried_cube.source = source
        queried_cube.config = str(cube_conf) if cube_conf else None
        queried_cube.db_config = str(dbConfig) if dbConfig else None
    else:
        cube = Cube(users=[current_user],
                    name=cube_name,
                    source=source,
                    config=str(cube_conf) if cube_conf else None,
                    db_config=str(dbConfig) if dbConfig else None
                    )
        db.session.add(cube)
    db.session.commit()


def cube_conf_to_file(data_request, save_path, source='csv', cube_name=None):
    """
    Temporary function
    :return:
    """
    facts = _gen_facts(data_request)
    dimensions = _gen_dimensions(data_request)
    cube = {
        'name': data_request['cubeName'] if not cube_name else cube_name,
        'source': source,
        'xmla_authentication': False,
        'facts': facts,
        'dimensions': dimensions
    }
    dbConfig = data_request['dbConfig']
    path = os.path.join(save_path, 'temp_config.yml')
    # try:
    with open(path, 'w') as yaml_file:
        yaml.safe_dump(cube, yaml_file)
        save_2_db(cube_name=cube['name'], source=cube['source'], cube_conf=cube, dbConfig=dbConfig)
    return path
    # except:
    #     return None


def try_construct_custom_files_cube(data_request):
    os.rename(os.path.join(TEMP_OLAPY_DIR, 'TEMP', TEMP_CUBE_NAME),
              os.path.join(TEMP_OLAPY_DIR, 'TEMP', data_request['cubeName']))
    temp_conf_file = cube_conf_to_file(data_request, TEMP_OLAPY_DIR)
    parser = ConfigParser()
    parsing_result = parser.get_cube_config(conf_file=temp_conf_file)
    executor = MdxEngine(cube_config=parsing_result, cubes_path=os.path.join(TEMP_OLAPY_DIR, 'TEMP'))
    try:
        executor.load_cube(data_request['cubeName'])
        if executor.star_schema_dataframe.columns is not None:
            return jsonify(executor.star_schema_dataframe.fillna('').head().to_html(classes=[
                'table-bordered table-striped'
            ], index=False))
    except:
        os.rename(os.path.join(TEMP_OLAPY_DIR, 'TEMP', data_request['cubeName']),
                  os.path.join(TEMP_OLAPY_DIR, 'TEMP', TEMP_CUBE_NAME))
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


def try_construct_custom_db_cube(data_request):
    temp_conf_file = cube_conf_to_file(data_request, TEMP_OLAPY_DIR, source='db',
                                       cube_name=data_request['dbConfig']['selectCube'])
    parser = ConfigParser()
    parsing_result = parser.get_cube_config(conf_file=temp_conf_file)
    db_config = get_db_config(data_request['dbConfig'])
    executor = MdxEngine(cube_config=parsing_result, database_config=db_config, source_type='db')
    # try:
    executor.load_cube(data_request['dbConfig']['selectCube'])
    if executor.star_schema_dataframe.columns is not None:
        return jsonify(executor.star_schema_dataframe.fillna('').head().to_html(classes=[
            'table-bordered table-striped'
        ], index=False))
    # except:
    #     return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/try_construct_custom_cube', methods=['POST'])
@login_required
def try_construct_custom_cube():
    if request.data and request.method == 'POST':
        data_request = json.loads(request.data)
        # todo temp, instead olapy with dict directly
        if data_request['dbConfig']:
            return try_construct_custom_db_cube(data_request)
        else:
            return try_construct_custom_files_cube(data_request)


@api('/cubes/confirm_custom_cube', methods=['POST'])
@login_required
def confirm_custom_cube():
    # try:
    confirm_cube(custom=True)
    os.rename(os.path.join(TEMP_OLAPY_DIR, 'temp_config.yml'),
              os.path.join(TEMP_OLAPY_DIR, 'cubes', 'cubes-config.yml'))
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
    # except:
    #     return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@api('/cubes/connectDB', methods=['POST'])
@login_required
def connectDB():
    if request.data and request.method == 'POST':
        data_request = json.loads(request.data)
        data_connection = {'driver': data_request['engine'].lower(),
                           'port': data_request['port'],
                           'password': data_request['password'],
                           'host': data_request['servername'],
                           'user': data_request['username'],
                           'dbms': data_request['engine']}
        executor = MdxEngine(source_type="db", database_config=data_connection)
        return jsonify(executor.get_cubes_names())


@api('/cubes/add_DB_cube', methods=['POST'])
@login_required
def add_db_cube():
    if request.method == 'POST':
        data = request.get_json()
        db_credentials = {
            'dbms': data['engine'].lower(),
            'user': data['username'],
            'password': data['password'],
            'host': data['servername'],
            'port': data['port'],
            'db_name': data['selectCube'],
        }

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


def todb2(data):
    config = {
        'dbms': data['engine'].lower(),
        'host': data['servername'],
        'port': data['port'],
        'user': data['username'],
        'password': data['password']
    }
    cube = Cube(users=[current_user], name=data['selectCube'], source='db', config=None,
                db_config=str(config))
    db.session.add(cube)
    db.session.commit()


@api('/cubes/confirm_db_cube', methods=['POST'])
@login_required
def confirm_db_cube():
    if request.method == 'POST':
        data = request.get_json()
        config = {
            'dbms': data['engine'].lower(),
            'host': data['servername'],
            'port': data['port'],
            'user': data['username'],
            'password': data['password']
        }
        path = os.path.join(TEMP_OLAPY_DIR, 'olapy-config.yml')
        try:
            with open(path, 'w') as yaml_file:
                yaml.safe_dump(config, yaml_file, default_flow_style=False)
                todb2(data)
                return jsonify(path)
        except:
            return None
