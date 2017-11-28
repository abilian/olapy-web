from __future__ import absolute_import, division, print_function, \
    unicode_literals

from olapy_web.app import create_app


def test_create_app():
    app = create_app()
    assert app
