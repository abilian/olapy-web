import json
from os import listdir

from os.path import isfile, join

TEST_CUBE = 'tests/test_cubes/sales'


def test_add_cube(client):
    files = [
        open(join(TEST_CUBE, file), 'r')
        for file in listdir(TEST_CUBE) if isfile(join(TEST_CUBE, file))
    ]

    response = client.post('api/cubes/add', data={
        'files': files,
    })
    result = json.loads(response.data)

    assert sorted(result['dimensions']) == sorted([u'tests/test_cubes/sales/Time.csv',
                                                   u'tests/test_cubes/sales/Facts.csv',
                                                   u'tests/test_cubes/sales/Product.csv',
                                                   u'tests/test_cubes/sales/Geography.csv'])
