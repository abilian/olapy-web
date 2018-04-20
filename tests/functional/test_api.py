import json
import os
from os import listdir

from os.path import isfile, join

from tests.utils import chart_data

CUBE_PATH = 'tests/demo_csv_cubes/sales'
CUSTOM_CUBE_PATH = 'tests/demo_csv_cubes/foodmart_with_config'


def test_add_csv_cube(client):
    with client:
        client.post('/login', data=dict(username="admin", password="admin"))

        files = [
            open(join(CUBE_PATH, file), 'rb') for file in listdir(CUBE_PATH)
            if isfile(join(CUBE_PATH, file))
        ]

        client.post('api/cubes/add', data={'files': files})
        request_data = {'customCube': False, 'cubeName': 'test'}
        client.post('api/cubes/confirm_cube', data=json.dumps(request_data))
        client.post('api/cubes/clean_tmp_dir')
        added_cube_result = client.get('api/cubes').data
        result = json.loads(added_cube_result)
        assert 'test' in result


def test_add_custom_csv_cube(client):
    with client:
        client.post('/login', data=dict(username="admin", password="admin"))
        current_dir = os.getcwd()
        os.chdir(CUSTOM_CUBE_PATH)  # to send files to server with their real names, not names as path
        files = [
            open(file, 'rb') for file in listdir(os.getcwd()) if isfile(file)
        ]
        os.chdir(current_dir)
        client.post('api/cubes/add', data={'files': files})

        request_data = {
            'cubeName': 'custom_test',
            'factsTable': 'food_facts.csv',
            'tablesAndColumnsResult': {
                'Product.csv': {
                    'DimCol': 'id',
                    'FactsCol': 'product_id'
                }
            },
            'columnsPerDimension': [],
            'measures': ['units_ordered'],
            'dbConfig': ''
        }

        client.post(
            'api/cubes/construct_custom_cube', data=json.dumps(request_data))

        request_data = {'cubeName': 'custom_test', 'customCube': True}

        client.post('api/cubes/confirm_cube', data=json.dumps(request_data))
        client.post('api/cubes/clean_tmp_dir')
        added_cube_result = client.get('api/cubes').data
        result = json.loads(added_cube_result)
        assert 'custom_test' in result


def test_add_db_cube(client):
    with client:
        client.post('/login', data=dict(username="admin", password="admin"))
        #  in the web , ypu don't put a string connection, instead each connexion param separately
        db_credentials = dict(
            selectCube='olapy_web_test',
            engine='postgres',
            servername='localhost',
            port='5432',
            username='postgres',
            password='root')
        client.post(
            'api/cubes/add_DB_cube',
            data=json.dumps(db_credentials),
            content_type='application/json')
        client.post(
            'api/cubes/confirm_db_cube',
            data=json.dumps(db_credentials),
            content_type='application/json')

        added_cube_result = client.get('api/cubes').data
        result = json.loads(added_cube_result)
        assert 'olapy_web_test' in result


def test_add_dashboard(client):
    with client:
        client.post('/login', data=dict(username='admin', password='admin'))

        dashboard_config = dict(
            dashboardName='dashboard_test',
            usedCharts=['pie'],
            layout=[{
                'x': 0,
                'y': 0,
                'w': 6,
                'h': 8,
                'i': "pie0"
            }],
            chartData=chart_data)
        response = client.post(
            'api/dashboard/save',
            data=json.dumps(dashboard_config),
            content_type='application/json')

        assert b'"success": true' in response.data
        all_dashboards = client.get('api/dashboard/all').data
        assert b"dashboard_test" in all_dashboards
        add_dashboard = json.loads(
            client.get('api/dashboard/dashboard_test').data)
        assert add_dashboard['name'] == 'dashboard_test'
        assert add_dashboard['used_charts'] == ['pie']
