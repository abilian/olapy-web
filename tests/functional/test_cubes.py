import json
from os import listdir

from os.path import isfile, join

TEST_CUBE = 'tests/test_cubes/sales'


def test_add_cube(client):
    with client:
        client.post('/login', data=dict(username="admin", password="admin"))

        files = [
            open(join(TEST_CUBE, file), 'rb') for file in listdir(TEST_CUBE)
            if isfile(join(TEST_CUBE, file))
        ]

        client.post('api/cubes/add', data={'files': files})
        request_data = {'customCube': False, 'cubeName': 'test'}
        client.post('api/cubes/confirm_cube', data=json.dumps(request_data))
        client.post('api/cubes/clean_tmp_dir')
        added_cube_result = client.get('api/cubes').data
        result = json.loads(added_cube_result)
        assert result == [u'test']
