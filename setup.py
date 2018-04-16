# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils import log

from os.path import realpath, join, dirname
from subprocess import check_output
from setuptools.command.sdist import sdist
from pkg_resources import parse_requirements
from setuptools import find_packages, setup, Command
from setuptools.command.develop import develop


_install_requires = parse_requirements(open("requirements.in"))
install_requires = [str(req) for req in _install_requires]

ROOT = realpath(join(dirname(__file__)))


class BuildStatic(Command):
    description = 'build static (front-end) files'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        front_dir = join(ROOT, 'front')
        # log.info("running 'npm install --quiet'")
        # check_output(['npm', 'install', '--quiet'], cwd=front_dir)

        log.info("running 'npm run build'")

        check_output(['yarn', 'build'], cwd=front_dir)


class SdistWithBuildStatic(sdist):

    def make_distribution(self):
        self.run_command('build_static')
        return sdist.make_distribution(self)


class DevelopWithBuildStatic(develop):

    def install_for_development(self):
        self.run_command('build_static')
        return develop.install_for_development(self)


setup(
    name='olapy_web',
    version="0.1.0",
    packages=find_packages(),
    author="Abilian SAS",
    author_email="contact@abilian.com",
    description="Front-end to OLAP Engine",
    url='https://github.com/abilian/olapy-web',
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
    # cmdclass={
    #     'build_static': BuildStatic,
    #     'develop': DevelopWithBuildStatic,
    #     'sdist': SdistWithBuildStatic,
    # }
)
