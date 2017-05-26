# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from os.path import expanduser

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages, setup



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
    classifiers=[
        "Programming Language :: Python",
        'Development Status :: 3 - Alpha',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        # "Topic :: Business intelligence",
    ],)

# TODO temp
os.system('pip install -e git+https://github.com/abilian/olapy.git@ab2a5d44e89aa055c9ac6c7d201284eca39a63f3#egg=olapy')

basedir = expanduser('~')
if not os.path.isfile(os.path.join(basedir,'olapy-data','olapy.db')):
    try:
        from olapy_web.manage import initdb
        initdb()
    except:
        raise ('unable to create users !')
