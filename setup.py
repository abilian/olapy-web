# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from pip.download import PipSession
from pip.req import parse_requirements


from setuptools import setup, find_packages
# from setuptools.command.develop import develop
# from setuptools.command.install import install


# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
#         # os.environ['olapy_path'] = "/home/mouadh/Musique2"
#         develop.run(self)
#         if not os.path.isfile(os.path.join(os.environ['OLAPY_PATH'], 'olapy-data', 'olapy.db')):
#         # if not os.path.isfile(os.path.join(basedir, 'olapy-data', 'olapy.db')):
#             # try:
#             from .manage import initdb
#             initdb()
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
#         install.run(self)
#         # basedir = expanduser('~')
#         # if not os.path.isfile(os.path.join(basedir, 'olapy-data', 'olapy.db')):
#         #     # try:
#         #     from manage import initdb
#         #     initdb()
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
    # cmdclass={
    #     'develop': PostDevelopCommand,
    #     'install': PostInstallCommand,
    # },
    include_package_data=False,
    classifiers=[
        "Programming Language :: Python",
        'Development Status :: 3 - Alpha',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        # "Topic :: Business intelligence",
    ],)


from web import app
os.environ['OLAPY_PATH'] = app.instance_path
os.system('pip install -e file:///home/mouadh/PycharmProjects/olapy/olapy')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.environ['OLAPY_PATH'],'olapy-data',
#                                                                     'olapy.db')
if not os.path.isfile(os.path.join(os.environ['OLAPY_PATH'], 'olapy-data', 'olapy.db')):
    from manage import initdb
    initdb()
