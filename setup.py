# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import zipfile

from pip.download import PipSession
from pip.req import parse_requirements


from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):

        develop.run(self)
        from web import app
        # TODO if server deployment do this
        os.system('export OLAPY_PATH=' + app.instance_path + ' ')
        os.environ['OLAPY_PATH'] = app.instance_path

        # KEEP !! so we can inject the instance_path
        # todo fix 2 olapy installation
        # os.system('pip install -e file:///home/mouadh/PycharmProjects/olapy/olapy')
        # os.system(
        #     'pip install -e git+https://github.com/abilian/olapy.git@86b7c7d99d4ba11f309660e73ad5d6e11cc89e22#egg=olapy')
        os.system(
            'pip install -e git+https://github.com/abilian/olapy.git@c85f307c2d64584959e56c9bc2d3de8395388b2e#egg=olapy')
        # zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
        # zip_ref.extractall(os.path.join(app.instance_path, 'olapy-data', 'cubes'))
        # zip_ref.close()

        if not os.path.isfile(os.path.join(app.instance_path, 'olapy-data', 'olapy.db')):
            from manage import initdb
            from web.models import User
            from web import db
            db.create_all()
            db.session.add(
                User(username="admin", email="admin@admin.com", password='admin'))
            db.session.add(
                User(username="demo", email="demo@demo.com", password="demo"))
            db.session.commit()
            # TODO fix conflict with flask_cli
            # initdb()

            # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)
        from web import app
        # TODO if server deployment do this
        os.system('export OLAPY_PATH=' + app.instance_path + ' ')
        os.environ['OLAPY_PATH'] = app.instance_path

        # KEEP !! so we can inject the instance_path
        # todo fix 2 olapy installation
        # os.system('pip install -e file:///home/mouadh/PycharmProjects/olapy/olapy')
        # os.system(
        #     'pip install -e git+https://github.com/abilian/olapy.git@86b7c7d99d4ba11f309660e73ad5d6e11cc89e22#egg=olapy')
        os.system(
            'pip install -e git+https://github.com/abilian/olapy.git@c85f307c2d64584959e56c9bc2d3de8395388b2e#egg=olapy')
        # zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
        # zip_ref.extractall(os.path.join(app.instance_path, 'olapy-data', 'cubes'))
        # zip_ref.close()

        if not os.path.isfile(os.path.join(app.instance_path, 'olapy-data', 'olapy.db')):
            from manage import initdb
            from web.models import User
            from web import db
            db.create_all()
            db.session.add(
                User(username="admin", email="admin@admin.com", password='admin'))
            db.session.add(
                User(username="demo", email="demo@demo.com", password="demo"))
            db.session.commit()
            # TODO fix conflict with flask_cli
            # initdb()

session = PipSession()
_install_requires = parse_requirements('requirements.txt', session=session)
install_requires = [str(ir.req) for ir in _install_requires]

setup(
    name='olapy_web',
    version="0.0.1",
    packages=find_packages(),
    author="Abilian SAS",
    author_email="contact@abilian.com",
    description="OLAP Engine",
    url='https://github.com/abilian/olapy',
    # TODO fix tox problem with path
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    include_package_data=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python",
        'Development Status :: 3 - Alpha',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        # "Topic :: Business intelligence",
    ],)