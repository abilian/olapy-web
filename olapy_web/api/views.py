# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import tempfile
from collections import OrderedDict
from distutils.dir_util import copy_tree
from os.path import expanduser, isdir
from pathlib import Path
from pprint import pprint

import pandas as pd
from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user
from olapy_web.extensions import db
from olapy_web.models import Chart, Cube, Dashboard, Pivottable, User
from six.moves.urllib.parse import urlunparse
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from werkzeug.utils import secure_filename

from olapy.core.mdx.executor.execute import MdxEngine

API = Blueprint("api", __name__, template_folder="templates")
api = API.route

ALLOWED_EXTENSIONS = {".csv"}
TEMP_CUBE_NAME = "TEMP_CUBE"
OLAPY_TEMP_DIR = os.path.join(tempfile.mkdtemp(), "TEMP")
home = expanduser("~")


def get_cube(cube_name):
    return (
        User.query.filter(User.id == current_user.id)
        .first()
        .cubes.filter(Cube.name == cube_name)
        .first()
    )


def get_cube_source_type(cube_name):
    cube_result = get_cube(cube_name)
    return cube_result.source


def get_config(cube_name):
    cube_result = get_cube(cube_name)
    return {
        "db_config": cube_result.db_config
        if cube_result and cube_result.db_config
        else None,
        "cube_config": cube_result.config
        if cube_result and cube_result.config
        else None,
    }


@api("/cubes")
def get_cubes():
    user_cubes = User.query.filter(User.id == current_user.id).first().cubes.all()
    return jsonify([cube.name for cube in user_cubes])


def _load_cube(cube_name):
    config = get_config(cube_name)
    source_type = get_cube_source_type(cube_name)
    if config["db_config"] == "sqlite://" and cube_name == "main":
        from tests.conftest import DEMO_DATABASE

        # not instantiating new engine , use test demo db, not passing serialized engine with post
        sqla_engine = DEMO_DATABASE
    elif config["db_config"]:
        sqla_engine = create_engine(config["db_config"])
    else:
        sqla_engine = None
    olapy_data_location = os.path.join(current_app.instance_path, "olapy-data")
    executor = MdxEngine(
        source_type=source_type,
        sqla_engine=sqla_engine,
        cube_config=config["cube_config"],
        olapy_data_location=olapy_data_location,
    )
    executor.load_cube(cube_name)
    return executor


@api("/cubes/<cube_name>/dimensions")
def get_cube_dimensions(cube_name):
    executor = _load_cube(cube_name)
    tables_names = executor.get_all_tables_names(ignore_fact=True)
    return jsonify(tables_names)


@api("/cubes/<cube_name>/facts")
def get_cube_facts(cube_name):
    cube = _load_cube(cube_name)
    cube_info = {"table_name": cube.facts, "measures": cube.measures}
    return jsonify(cube_info)


def allowed_file(filename):
    file_extension = Path(filename).suffix
    return file_extension in ALLOWED_EXTENSIONS


def clean_temp_dir(olapy_data_dir):
    for the_file in os.listdir(olapy_data_dir):
        file_path = os.path.join(olapy_data_dir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def construct_cube(
    cube_name, sqla_engine=None, source_type="csv", olapy_data_location=None
):
    executor = MdxEngine(
        sqla_engine=sqla_engine,
        source_type=source_type,
        olapy_data_location=olapy_data_location,
        cubes_folder="",
    )
    # try to construct automatically the cube
    try:
        executor.load_cube(cube_name)
        return {
            "dimensions": executor.get_all_tables_names(ignore_fact=True),
            "facts": executor.facts,
            "measures": executor.measures,
        }
    except (IOError, ProgrammingError):  # Facts does not exist
        return {"all_tables": executor.get_all_tables_names(ignore_fact=False)}


@api("/cubes/add", methods=["POST"])
def add_cube():
    # temporary
    #  2 TEMP_CUBE_NAME = first is the all cubes folder, the second is the current cube folder
    cube_dir = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME)
    if isdir(cube_dir):
        clean_temp_dir(cube_dir)
    else:
        os.makedirs(cube_dir)
    all_file = request.files.getlist("files")
    for file_uploaded in all_file:
        if file_uploaded and allowed_file(file_uploaded.filename):
            filename = secure_filename(file_uploaded.filename)
            file_uploaded.save(os.path.join(cube_dir, filename))
    cube = construct_cube(
        cube_name=TEMP_CUBE_NAME, olapy_data_location=OLAPY_TEMP_DIR, source_type="csv"
    )
    if "dimensions" in cube:
        return jsonify(cube)
    else:
        return jsonify(
            {
                "facts": None,
                "dimensions": [file.filename for file in all_file],
                "measures": None,
            }
        )


@api("/cubes/confirm_cube", methods=["POST"])
def confirm_cube():
    if request.data:
        request_data = request.json
        custom_cube = request_data.get("customCube")
        cube_name = request_data.get("cubeName")
        if custom_cube:
            temp_folder = cube_name
        else:
            temp_folder = TEMP_CUBE_NAME
            save_cube_config_2_db(config=None, cube_name=cube_name, source="csv")
        new_temp_dir = os.path.join(OLAPY_TEMP_DIR, temp_folder)
        if isdir(new_temp_dir):
            olapy_data_dir = os.path.join(
                current_app.instance_path, "olapy-data", "cubes", cube_name
            )
            copy_tree(new_temp_dir, olapy_data_dir)
            shutil.rmtree(new_temp_dir)
            # custom -> config with config file , no need to return response,
            # instead wait to use the cube conf
        return jsonify({"success": True}), 200


@api("/cubes/clean_tmp_dir", methods=["POST"])
def clean_tmp_dir():
    for root, dirs, files in os.walk(OLAPY_TEMP_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return jsonify({"success": True}), 200


def get_columns_from_files(db_cube_config):
    if isdir(OLAPY_TEMP_DIR):
        cube_file_path = os.path.join(
            OLAPY_TEMP_DIR, TEMP_CUBE_NAME, db_cube_config["tableName"]
        )
        df = pd.read_csv(cube_file_path, sep=";")
        # todo show columns with there types
        if db_cube_config["WithID"]:
            result = [column for column in df.columns]
        else:
            result = [
                column
                for column in df.columns
                if "_id" not in column.lower()[-3:] and "id" != column.lower()
            ]
        return result


def get_columns_from_db(db_cube_config):
    sqla_uri = generate_sqla_uri(db_cube_config["dbConfig"])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(sqla_engine=sqla_engine, source_type="db")
    results = executor.sqla_engine.execution_options(stream_results=True).execute(
        "SELECT * FROM {}".format(db_cube_config["tableName"])
    )
    df = pd.DataFrame(iter(results), columns=results.keys())
    if db_cube_config["WithID"]:
        result = [column for column in df.columns]
    else:
        result = [
            column
            for column in df.columns
            if "_id" not in column.lower()[-3:] and "id" != column.lower()
        ]
    return result


@api("/cubes/get_table_columns", methods=["POST"])
def get_table_columns():
    db_cube_config = request.json
    if db_cube_config:
        if db_cube_config["dbConfig"]:
            return jsonify(get_columns_from_db(db_cube_config))
        else:
            return jsonify(get_columns_from_files(db_cube_config))
    raise Exception("cube config is not specified")


def get_tables_columns_from_db(db_cube_config):
    response = {}
    sqla_uri = generate_sqla_uri(db_cube_config["dbConfig"])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(sqla_engine=sqla_engine, source_type="db")
    att_tables = db_cube_config["allTables"].split(",")
    for table_name in att_tables:
        results = executor.sqla_engine.execution_options(stream_results=True).execute(
            "SELECT * FROM {}".format(table_name)
        )
        df = pd.DataFrame(iter(results), columns=results.keys())
        response[table_name] = list(df.columns)
    return response


def get_tables_columns_from_files(db_cube_config):
    if isdir(OLAPY_TEMP_DIR):
        response = {}
        att_tables = db_cube_config["allTables"].split(",")
        for table_name in att_tables:
            file_path = os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME, table_name)
            df = pd.read_csv(file_path, sep=";")
            response[table_name] = list(df.columns)
        return response


@api("/cubes/get_tables_and_columns", methods=["POST"])
def get_tables_and_columns():
    if request.data:
        # db_cube_config = json.loads(request.data.decode('utf-8'))
        db_cube_config = request.json
        if db_cube_config["dbConfig"]:
            return jsonify(get_tables_columns_from_db(db_cube_config))
        else:
            return jsonify(get_tables_columns_from_files(db_cube_config))
    raise Exception("cube config is not specified")


def _gen_facts(data_request):
    """
    TEMPORARY
    :param data_request:
    :return:
    """
    columns_names = []
    refs = []
    for table in data_request["tablesAndColumnsResult"]:
        columns_names.append(data_request["tablesAndColumnsResult"][table]["FactsCol"])
        refs.append(
            table.replace(".csv", "")
            + "."
            + data_request["tablesAndColumnsResult"][table]["DimCol"]
        )

    keys = dict((column, refs[index]) for (index, column) in enumerate(columns_names))
    return {
        "table_name": data_request["factsTable"].replace(".csv", ""),
        "keys": keys,
        "measures": data_request["measures"],
    }


def check_specified_table_column(table_name, data_request):
    columns = OrderedDict()
    for table_col in data_request["columnsPerDimension"]:
        if table_col and table_col["table"].replace(".csv", "") == table_name:
            for column in table_col["columns"]:
                columns.update({column: column})
    return columns


def _gen_dimensions(data_request):
    """
    TEMPORARY
    :param data_request:
    :return:
    """
    facts_table = data_request["factsTable"].replace(".csv", "")
    dimensions = [{"name": facts_table, "displayName": facts_table}]
    for table in data_request["tablesAndColumnsResult"]:
        table_name = table.replace(".csv", "")
        columns = check_specified_table_column(table_name, data_request)
        dimensions.append(
            {"name": table_name, "displayName": table_name, "columns": columns}
        )

    return dimensions


@api("/pivottable/delete", methods=["POST"])
@api("/cubes/delete", methods=["POST"])
@api("/dashboard/delete", methods=["POST"])
def delete():
    request_data = request.get_json()
    connected_user = User.query.filter(User.id == current_user.id).first()
    queried_obj = request.environ.get("PATH_INFO").split("/")[-2]
    if queried_obj.upper() == "CUBES":
        obj = connected_user.cubes.filter(Cube.name == request_data["cubeName"]).first()
    elif queried_obj.upper() == "DASHBOARD":
        obj = connected_user.dashboards.filter(
            Dashboard.name == request_data["dashboardName"]
        ).first()
    elif queried_obj.upper() == "PIVOTTABLE":
        obj = connected_user.pivottables.filter(
            Pivottable.name == request_data["pivottableName"]
        ).first()
    else:
        obj = None

    if obj:
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"success": True}), 200


def save_cube_config_2_db(config, cube_name, source):
    queried_cube = (
        User.query.filter(User.id == current_user.id)
        .first()
        .cubes.filter(Cube.name == cube_name)
        .first()
    )
    # config can be None
    cube_config = config.get("cube_config") if config else None
    db_config = config.get("db_config") if config else None
    if queried_cube:
        # update cube
        queried_cube.name = cube_name
        queried_cube.source = source
        queried_cube.config = cube_config
        queried_cube.db_config = db_config
    else:
        # add new cube
        cube = Cube(
            users=[current_user],
            name=cube_name,
            source=source,
            config=cube_config,
            db_config=db_config,
        )
        db.session.add(cube)
    db.session.commit()


def gen_cube_conf(data_request, source="csv", cube_name=None):
    """
    Temporary function
    :return:
    """
    facts = _gen_facts(data_request)
    dimensions = _gen_dimensions(data_request)
    cube_conf = {
        "name": data_request["cubeName"] if not cube_name else cube_name,
        "source": source,
        "xmla_authentication": False,
        "facts": facts,
        "dimensions": dimensions,
    }
    if data_request.get("dbConfig"):
        db_config = generate_sqla_uri(data_request.get("dbConfig"))
    else:
        db_config = None

    return {"cube_config": cube_conf, "db_config": db_config}


def construct_custom_files_cube(data_request):
    os.rename(
        os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME),
        os.path.join(OLAPY_TEMP_DIR, data_request["cubeName"]),
    )
    cube_config = gen_cube_conf(
        data_request=data_request, cube_name=data_request["cubeName"]
    )
    executor = MdxEngine(
        cube_config=cube_config["cube_config"],
        olapy_data_location=OLAPY_TEMP_DIR,
        cubes_folder="",
    )
    # try:
    executor.load_cube(data_request["cubeName"])
    if executor.star_schema_dataframe.columns is not None:
        save_cube_config_2_db(cube_config, data_request["cubeName"], source="csv")
        return (
            executor.star_schema_dataframe.fillna("")
            .head()
            .to_html(classes=["table-bordered table-striped"], index=False)
        )
    # except:
    #     os.rename(
    #         os.path.join(OLAPY_TEMP_DIR, data_request['cubeName']),
    #         os.path.join(OLAPY_TEMP_DIR, TEMP_CUBE_NAME))
    #     return None


def construct_custom_db_cube(data_request):
    config = gen_cube_conf(
        data_request, source="db", cube_name=data_request["dbConfig"]["selectCube"]
    )
    source_type = "db"
    sqla_uri = generate_sqla_uri(data_request["dbConfig"])
    sqla_engine = create_engine(sqla_uri)
    executor = MdxEngine(
        source_type=source_type,
        sqla_engine=sqla_engine,
        cube_config=config["cube_config"],
    )
    # try:
    executor.load_cube(data_request["dbConfig"]["selectCube"])
    if executor.star_schema_dataframe.columns is not None:
        save_cube_config_2_db(
            config, data_request["dbConfig"]["selectCube"], source="db"
        )
        return (
            executor.star_schema_dataframe.fillna("")
            .head()
            .to_html(classes=["table-bordered table-striped"], index=False)
        )
    # except:
    #     return None


@api("/cubes/construct_custom_cube", methods=["POST"])
def construct_custom_cube():
    if request.data:
        data_request = request.json
        if data_request["dbConfig"]:
            star_schema_table = construct_custom_db_cube(data_request)
        else:
            star_schema_table = construct_custom_files_cube(data_request)
        if star_schema_table:
            return jsonify(star_schema_table)
        else:
            raise Exception("unable to construct cube")


def generate_sqla_uri(db_credentials):
    engine = db_credentials.get("engine").lower().replace("postgres", "postgresql")
    user = db_credentials.get("username")
    password = db_credentials.get("password")
    server = db_credentials.get("servername")
    port = db_credentials.get("port")
    if not user and not server and db_credentials["selectCube"] == "main":
        selected_cube = "//"
    else:
        selected_cube = db_credentials.get("selectCube", "")
    if password:
        password = ":" + password
    if port:
        port = ":" + port
    if server:
        server = "@" + server
    netloc = user + password + server + port
    print(urlunparse((engine, netloc, selected_cube, "", "", "")))
    return urlunparse((engine, netloc, selected_cube, "", "", ""))


@api("/cubes/connectDB", methods=["POST"])
def connectDB():
    if request.data:
        sqla_uri = generate_sqla_uri(request.json)
        sqla_engine = create_engine(sqla_uri)
        executor = MdxEngine(source_type="db", sqla_engine=sqla_engine)
        return jsonify(executor.get_cubes_names())


@api("/cubes/add_DB_cube", methods=["POST"])
def add_db_cube():
    request_data = request.get_json()
    if (
        not request.json.get("servername")
        and not request.json.get("username")
        and request.json.get("engine") == "sqlite"
    ):
        from tests.conftest import DEMO_DATABASE

        sqla_engine = DEMO_DATABASE
    #     for test use demo database sqla engine not creating new one ,
    #     and not passing the engine with the post
    else:
        sqla_uri = generate_sqla_uri(request.json)
        sqla_engine = create_engine(sqla_uri)

    construction = construct_cube(
        cube_name=request_data["selectCube"],
        source_type="db",
        sqla_engine=sqla_engine,
        olapy_data_location=current_app.instance_path,
    )
    if "dimensions" in construction:
        return jsonify(construction)
    else:
        return jsonify(
            {"facts": None, "dimensions": construction["all_tables"], "measures": None}
        )


@api("/cubes/confirm_db_cube", methods=["POST"])
def confirm_db_cube():
    request_data = request.get_json()
    config = {"cube_config": None, "db_config": generate_sqla_uri(request_data)}
    save_cube_config_2_db(
        config=config, cube_name=request_data["selectCube"], source="db"
    )
    return jsonify({"success": True}), 200


@api("/cubes/chart_columns", methods=["POST"])
def get_chart_columns_result():
    request_data = request.get_json()
    executor = _load_cube(request_data["selectedCube"])
    return (
        executor.star_schema_dataframe.groupby([request_data["selectedColumn"]])
        .sum()[request_data["selectedMeasures"]]
        .to_json()
    )


@api("/cubes/<cube_name>/columns")
def get_cube_columns(cube_name):
    executor = _load_cube(cube_name)
    return jsonify(
        [
            column
            for column in executor.star_schema_dataframe.columns
            if column.lower()[-3:] != "_id" and column not in executor.measures
        ]
    )


@api("/dashboard/save", methods=["POST"])
def save_dashboard():
    request_data = request.get_json()
    user_dashboard = (
        User.query.filter(User.id == current_user.id)
        .first()
        .dashboards.filter(Dashboard.name == request_data["dashboardName"])
        .first()
    )
    if user_dashboard:
        # update dashboard
        user_dashboard.name = request_data["dashboardName"]
        user_dashboard.chart.used_charts = request_data["usedCharts"]
        user_dashboard.chart.charts_layout = request_data["layout"]
        user_dashboard.chart.charts_data = request_data["chartData"]
    else:
        # add new cube
        chart = Chart(
            used_charts=request_data["usedCharts"],
            charts_layout=request_data["layout"],
            charts_data=request_data["chartData"],
        )
        dashboard = Dashboard(
            name=request_data["dashboardName"], user_id=current_user.id, chart=chart
        )
        db.session.add(dashboard)
    db.session.commit()
    return jsonify({"success": True}), 200


@api("/dashboard/all")
def all_dashboard():
    all_dashboards = User.query.filter(User.id == current_user.id).first().dashboards
    return jsonify([dashboard.name for dashboard in all_dashboards])


@api("/dashboard/<dashboard_name>")
def get_dashboard(dashboard_name):
    dashboard = (
        User.query.filter(User.id == current_user.id)
        .first()
        .dashboards.filter(Dashboard.name == dashboard_name)
        .first()
    )
    return jsonify(
        {
            "name": dashboard.name,
            "used_charts": dashboard.chart.used_charts,
            "charts_layout": dashboard.chart.charts_layout,
            "charts_data": dashboard.chart.charts_data,
        }
    )


@api("/query_builder/<cube>")
def star_schema_df_query_builder(cube):
    executor = _load_cube(cube)
    return jsonify(executor.star_schema_dataframe.to_csv(encoding="utf-8"))


@api("/pivottable/save", methods=["POST"])
def save_pivottable():
    request_data = request.get_json()
    user_pivottable = (
        User.query.filter(User.id == current_user.id)
        .first()
        .pivottables.filter(Pivottable.name == request_data["pivottableName"])
        .first()
    )
    selected_cube = Cube.query.filter(
        User.id == current_user.id, Cube.name == request_data["cubeName"]
    ).first()
    if user_pivottable:
        user_pivottable.name = request_data["pivottableName"]
        user_pivottable.rows = request_data["pvtRows"]
        user_pivottable.columns = request_data["pvtCols"]
    else:
        pivottable = Pivottable(
            user_id=current_user.id,
            name=request_data["pivottableName"],
            rows=request_data["pvtRows"],
            columns=request_data["pvtCols"],
            cube=selected_cube,
        )
        db.session.add(pivottable)
    db.session.commit()
    return jsonify({"success": True}), 200


@api("/pivottable/<pivottable_name>")
def get_pivottable(pivottable_name):
    pivottable = (
        User.query.filter(User.id == current_user.id)
        .first()
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


@api("/pivottable/all")
def all_pivottables():
    all_pivottables = User.query.filter(User.id == current_user.id).first().pivottables
    return jsonify([pivottable.name for pivottable in all_pivottables])
