# -*- encoding: utf8 -*-
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os

from six import text_type
from typing import Any, Union

import numpy as np
import pandas as pd
from flask import Blueprint, Response, current_app, flash, redirect, \
    render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from olapy.core.mdx.executor.execute import MdxEngine

from app.tools.config_file_parser import ConfigParser
from .extensions import login_manager
from .forms import LoginForm
from .models import User
import importlib

blueprint = Blueprint('main', __name__, template_folder='templates')
route = blueprint.route


def _build_charts(dashboard, executer):
    graphs = {}
    for chart_type, chart_attributs in dashboard.items():
        if chart_type == 'global_table':
            continue
        ChartClass = getattr(importlib.import_module("app.tools.models"), chart_type[:-1])
        chart = ChartClass(executer, chart_attributs)
        graphs[chart_type.lower().replace('charts', '')] = chart.gen_graphs()
    return graphs


@login_manager.user_loader
def load_user(userid):
    # type: (Any) -> User
    """Load user with specific id.
    """
    return User.query.get(int(userid))


@route('/index')
@route('/')
def index():
    # type: () -> Response
    return redirect('/query_builder')
    # return render_template('execute_query.html',user=current_user)


@route('/login', methods=['GET', 'POST'])
def login():
    # type: () -> Union[Response, text_type]
    """Login user.
    """
    form = LoginForm()
    if len(form.errors) > 0:
        flash(form.errors)
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            # next to hold the the page that the user tries to visite

            next_url = request.args.get('next') or url_for(
                'dashboard', user=current_user)
            return redirect(next_url)

        flash('incorrect username or password')

    return render_template('login.html', form=form, user=current_user)


@route('/logout')
def logout():
    # type: () -> Response
    """Logout user.
    """
    logout_user()
    return redirect(url_for('.login'))


@route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # type: () -> text_type
    """Generate Dashboard with charts from web_config_file.
    """
    olapy_data_location = os.path.join(current_app.instance_path, 'olapy-data')

    web_config_file_path = os.path.join(olapy_data_location, 'cubes', 'web_cube_config.yml')
    config = ConfigParser(web_config_file_path)
    dashboard = config.construct_web_dashboard()

    config = ConfigParser(web_config_file_path)
    cube_config_file = config.construct_cubes()

    executor = MdxEngine(cube_config=cube_config_file,
                         olapy_data_location=olapy_data_location)
    executor.load_cube(cube_config_file['name'])

    if not dashboard:
        return ('<h3> your config file (' + web_config_file_path +
                ') does not contains dashboard section </h3>')

    graphs = _build_charts(dashboard, executor)
    # todo margins = True ( prob )
    pivot_table_df = pd.pivot_table(
        executor.star_schema_dataframe,
        values=executor.measures,
        index=dashboard['global_table']['columns'],
        columns=dashboard['global_table']['rows'],
        aggfunc=np.sum)
    return render_template(
        'dashboard.html',
        table_result=pivot_table_df.fillna('').to_html(classes=[
            'table m-0 table-primary table-colored table-bordered table-hover table-striped display'
        ]),
        graphs=graphs,
        user=current_user)


@route('/query_builder', methods=['GET', 'POST'])
@login_required
def query_builder():
    # type: () -> text_type
    """Generates web pivot table based on Olapy star_schema_DataFrame.

    :return: pivottable.js
    """

    olapy_data_location = os.path.join(current_app.instance_path, 'olapy-data')

    web_config_file_path = os.path.join(olapy_data_location, 'cubes', 'web_cube_config.yml')
    config = ConfigParser(web_config_file_path)
    cube_config_file = config.construct_cubes()  # one cube right now
    executor = MdxEngine(cube_config=cube_config_file,
                         olapy_data_location=olapy_data_location)
    executor.load_cube(cube_config_file['name'])

    return render_template('query_builder.html',
                           user=current_user,
                           dataframe_csv=executor.star_schema_dataframe.to_csv(encoding="utf-8"))


@route('/designer', methods=['GET', 'POST'])
@login_required
def schema_designer():
    executor = MdxEngine()
    cubes_names = executor.get_cubes_names()
    return render_template('schema_designer.html',
                           user=current_user,
                           user_cubes=cubes_names)


@route('/reporting', methods=['GET', 'POST'])
@login_required
def reporting():
    executor = MdxEngine()
    cubes_names = executor.get_cubes_names()
    return render_template('reporting.html',
                           user=current_user,
                           user_cubes=cubes_names)
