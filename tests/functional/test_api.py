from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
from os import listdir
from os.path import isfile, join

from tests.utils import chart_data

from olapy_web.api.views import get_config, get_cube_source_type

CUBE_PATH = "tests/demo_csv_cubes/sales"
CUSTOM_CUBE_PATH = "tests/demo_csv_cubes/foodmart_with_config"


def test_add_csv_cube(client):
    with client:
        client.post("/login", data={"username": "admin", "password": "admin"})

        files = [
            open(join(CUBE_PATH, file), "rb")
            for file in listdir(CUBE_PATH)
            if isfile(join(CUBE_PATH, file))
        ]

        client.post("api/cubes/add", data={"files": files})
        request_data = {"customCube": False, "cubeName": "test"}
        client.post("api/cubes/confirm_cube", json=request_data)
        client.post("api/cubes/clean_tmp_dir")
        added_cube_result = client.get("api/cubes").get_json()
        assert "test" in added_cube_result
        assert get_cube_source_type("test") == "csv"


def test_add_custom_csv_cube(client):
    with client:
        client.post("/login", data={"username": "admin", "password": "admin"})
        current_dir = os.getcwd()
        os.chdir(
            CUSTOM_CUBE_PATH
        )  # to send files to server with their real names, not names as path
        files = [open(file, "rb") for file in listdir(os.getcwd()) if isfile(file)]
        os.chdir(current_dir)
        client.post("api/cubes/add", data={"files": files})

        request_data = {"WithID": False, "tableName": "food_facts.csv", "dbConfig": ""}
        columns = client.post(
            "api/cubes/get_table_columns", json=request_data
        ).get_json()

        assert columns == [
            "units_ordered",
            "units_shipped",
            "warehouse_sales",
            "warehouse_cost",
            "supply_time",
            "store_invoice",
        ]

        request_data = {
            "cubeName": "custom_test",
            "factsTable": "food_facts.csv",
            "tablesAndColumnsResult": {
                "Product.csv": {"DimCol": "id", "FactsCol": "product_id"}
            },
            "columnsPerDimension": [],
            "measures": ["units_ordered"],
            "dbConfig": "",
        }

        client.post("api/cubes/construct_custom_cube", json=request_data)

        request_data = {"cubeName": "custom_test", "customCube": True}

        client.post("api/cubes/confirm_cube", json=request_data)
        client.post("api/cubes/clean_tmp_dir")
        added_cube_result = client.get("api/cubes").get_json()
        assert "custom_test" in added_cube_result
        cube_config = get_config("custom_test")["cube_config"]
        assert cube_config["name"] == "custom_test"


def test_add_db_cube(client):
    with client:
        client.post("/login", data=dict(username="admin", password="admin"))
        #  in the web , ypu don't put a string connection, instead each connexion param separately
        db_credentials = dict(
            selectCube="main",
            engine="sqlite",
            servername="",
            port="",
            username="",
            password="",
        )

        client.post(
            "api/cubes/add_DB_cube",
            json=db_credentials,
            content_type="application/json",
        )
        client.post(
            "api/cubes/confirm_db_cube",
            json=db_credentials,
            content_type="application/json",
        )

        added_cube_result = client.get("api/cubes").get_json()
        assert "main" in added_cube_result
        facts_details = client.get("api/cubes/main/facts").get_json()
        excpected_facts_details = {
            "measures": ["amount", "count"],
            "table_name": "Facts",
        }
        assert facts_details == excpected_facts_details

        dimensions_details = client.get("api/cubes/main/dimensions").get_json()
        excpected_dimensions_details = ["product", "time", "geography"]

        assert sorted(dimensions_details) == sorted(excpected_dimensions_details)


def test_add_dashboard(client):
    with client:
        client.post("/login", data=dict(username="admin", password="admin"))

        dashboard_config = dict(
            dashboardName="dashboard_test",
            usedCharts=["pie"],
            layout=[{"x": 0, "y": 0, "w": 6, "h": 8, "i": "pie0"}],
            chartData=chart_data,
        )
        response = client.post(
            "api/dashboard/save", json=dashboard_config, content_type="application/json"
        )
        response_state = response.get_json()
        assert response_state["success"]

        all_dashboards = client.get("api/dashboard/all").data
        assert b"dashboard_test" in all_dashboards

        add_dashboard = client.get("api/dashboard/dashboard_test").get_json()
        assert add_dashboard["name"] == "dashboard_test"
        assert add_dashboard["used_charts"] == ["pie"]
