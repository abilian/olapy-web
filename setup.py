# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from os.path import expanduser

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages, setup


from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
        print('111111111111111111111111')
        develop.run(self)

        basedir = expanduser('~')
        if not os.path.isfile(os.path.join(basedir, 'olapy-data', 'olapy.db')):
            # try:
            from manage import initdb
            initdb()
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
        print('2222222222222222222222222')
        install.run(self)

        basedir = expanduser('~')
        if not os.path.isfile(os.path.join(basedir, 'olapy-data', 'olapy.db')):
            # try:
            from manage import initdb
            initdb()
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION



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

session = PipSession()
_install_requires = parse_requirements('requirements.txt', session=session)
install_requires = [str(ir.req) for ir in _install_requires]


# TODO temp
# os.system('pip install -e git+https://github.com/abilian/olapy.git@b0e89794d508b20c8d2abe60311f5f735be3aa8c#egg=olapy')
#
# basedir = expanduser('~')
# if not os.path.isfile(os.path.join(basedir,'olapy-data','olapy.db')):
#     # try:
#     from manage import initdb
#     initdb()
    # from web.models import User
    #
    # from web import db
    # db.create_all()
    # db.session.add(
    #     User(username="admin", email="admin@admin.com", password='admin'))
    # db.session.add(
    #     User(username="demo", email="demo@demo.com", password="demo"))
    # db.session.commit()
    # print('Initialized the database')
    # except:
    #     raise ('unable to create users !')
