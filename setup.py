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
        os.system(
            'pip install -e git+https://github.com/abilian/olapy.git@52962cefc005c712a0e8157bb1a6367e590995d6#egg=olapy')
        # os.system(
        #     'pip install -e git+https://github.com/abilian/olapy.git@627438ac626536d4aca38664ad0895f118a7fe2e#egg=olapy')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.environ['OLAPY_PATH'],'olapy-data',
        #                                                                     'olapy.db')
        # if not os.path.isfile(os.path.join(os.environ['OLAPY_PATH'], 'olapy-data', 'olapy.db')):

        # zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
        # zip_ref.extractall(os.path.join(app.instance_path, 'olapy-data', 'cubes'))
        # zip_ref.close()

        if not os.path.isfile(os.path.join(app.instance_path, 'olapy-data', 'olapy.db')):
            from manage import initdb
            initdb()

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
        os.system(
            'pip install -e git+https://github.com/abilian/olapy.git@52962cefc005c712a0e8157bb1a6367e590995d6#egg=olapy')
        # os.system(
        #     'pip install -e git+https://github.com/abilian/olapy.git@627438ac626536d4aca38664ad0895f118a7fe2e#egg=olapy')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.environ['OLAPY_PATH'],'olapy-data',
        #                                                                     'olapy.db')
        # if not os.path.isfile(os.path.join(os.environ['OLAPY_PATH'], 'olapy-data', 'olapy.db')):
        # zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
        # zip_ref.extractall(os.path.join(app.instance_path, 'olapy-data', 'cubes'))
        # zip_ref.close()

        if not os.path.isfile(os.path.join(app.instance_path, 'olapy-data', 'olapy.db')):
            from manage import initdb
            initdb()



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