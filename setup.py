# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages, setup

session = PipSession()
_install_requires = parse_requirements('requirements.in', session=session)
install_requires = [str(ir.req) for ir in _install_requires]

setup(
    name='olapy_web',
    version="0.1.0",
    packages=find_packages(),
    author="Abilian SAS",
    author_email="contact@abilian.com",
    description="Front-end to OLAP Engine",
    url='https://github.com/abilian/olapy-web',
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
    ],
)
