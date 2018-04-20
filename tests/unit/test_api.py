import json
from os import listdir

from os.path import isfile, join

from tests.utils import chart_data

TEST_CUBE = 'tests/demo_csv_cubes/sales'


def test_upload_cube(client):
    files = [
        open(join(TEST_CUBE, file), 'rb') for file in listdir(TEST_CUBE)
        if isfile(join(TEST_CUBE, file))
    ]

    response = client.post(
        'api/cubes/add', data={
            'files': files,
        })
    result = json.loads(response.data)

    assert sorted(result['dimensions']) == sorted([
        u'tests/demo_csv_cubes/sales/Time.csv',
        u'tests/demo_csv_cubes/sales/Facts.csv',
        u'tests/demo_csv_cubes/sales/Product.csv',
        u'tests/demo_csv_cubes/sales/Geography.csv'
    ])


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
        response = client.post(
            'api/cubes/add_DB_cube',
            data=json.dumps(db_credentials),
            content_type='application/json').data
        cube = json.loads(response)
        assert sorted(cube['dimensions']) == sorted(
            ['geography', 'product', 'time'])
        assert sorted(cube['measures']) == sorted(['amount', 'count'])


def test_add_dashboard(client):
    with client:
        client.post('/login', data=dict(username="admin", password="admin"))

        dashboard_config = dict(
            dashboardName='dashboard_test',
            usedCharts=['pie'],
            layout=[{'x': 0, 'y': 0, 'w': 6, 'h': 8, 'i': "pie0"}],
            chartData=chart_data)
        response = client.post(
            'api/dashboard/save',
            data=json.dumps(dashboard_config),
            content_type='application/json')

        assert b'"success": true' in response.data
