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
from olapy.core.mdx.tools.config_file_parser import ConfigParser

from .extensions import login_manager
from .forms import LoginForm
from .models import User
from .pivottable import pivot_ui
from .stats_utils import GraphsGen

blueprint = Blueprint('main', __name__, template_folder='templates')
route = blueprint.route


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


def _build_charts(dashboard, executer):
    graph_gen = GraphsGen()
    graphs = {}
    star_dataframe = executer.get_star_schema_dataframe()

    for chart_type, chart_attributs in dashboard.__dict__.items():
        all_dataframes = []
        tables_names = []
        total = {}
        if chart_type == 'pie_charts':
            for chart_table_column in chart_attributs:
                total[chart_table_column] = star_dataframe[
                    chart_table_column].value_counts().sum()
                df = star_dataframe[
                    chart_table_column].value_counts().to_frame().reset_index()
                all_dataframes.append(df)
                tables_names.append(chart_table_column)

            graphs['pie_charts'] = {
                'graphs': graph_gen.generate_pie_graphes(all_dataframes),
                'totals': total,
                'tables_names': tables_names
            }

        elif chart_type == 'bar_charts':
            for measure in executer.measures:
                total[measure] = star_dataframe[measure].sum()
            for chart_table_column in chart_attributs:
                df = star_dataframe[[chart_table_column] +
                                    executer.measures].groupby([
                                        chart_table_column
                                    ]).sum().reset_index()
                all_dataframes.append(df)
                tables_names.append(chart_table_column)

            graphs['bar_charts'] = {
                'graphs': graph_gen.generate_bar_graphes(all_dataframes),
                'totals': total,
                'tables_names': tables_names
            }

        elif chart_type == 'line_charts':
            for measure in executer.measures:
                total[measure] = star_dataframe[measure].sum()

            for column_name, columns_attributs in chart_attributs.items():
                df = star_dataframe[[column_name] + executer.measures].groupby(
                    [column_name]).sum().reset_index()

                # filter columns to show
                if columns_attributs is not 'ALL':
                    df = df[df[column_name].isin(columns_attributs)]

                tables_names.append(column_name)
                all_dataframes.append(df)

            graphs['line_charts'] = {
                'graphs': graph_gen.generate_line_graphes(all_dataframes),
                'totals': total,
                'tables_names': tables_names
            }

    return graphs


@route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # type: () -> text_type
    """Generate Dashboard with charts from web_config_file.
    """
    # TODO use plotly dashboard !!!
    cubes_path = os.path.join(current_app.instance_path, 'olapy-data', 'cubes')
    config = ConfigParser(cube_path=cubes_path)
    executer = MdxEngine(
        cube_name=list(config.get_cubes_names(client_type='web').keys())[0],
        cubes_path=cubes_path,
        client_type='web')
    dashboard = config.construct_web_dashboard()
    if not dashboard:
        config_path = os.path.join(config.cube_path,
                                   config.web_config_file_name)
        return ('<h3> your config file (' + config_path +
                ') does not contains dashboard section </h3>')
    else:
        # first dashboard only right now
        dashboard = dashboard[0]

    graphs = _build_charts(dashboard, executer)
    # todo margins = True ( prob )
    pivot_table_df = pd.pivot_table(
        executer.get_star_schema_dataframe(),
        values=executer.measures,
        index=dashboard.global_table['columns'],
        columns=dashboard.global_table['rows'],
        aggfunc=np.sum)

    return render_template(
        'dashboard.html',
        table_result=pivot_table_df.fillna('').to_html(classes=[
            'table m-0 table-primary table-colored table-bordered table-hover table-striped display'
        ]),
        pies=graphs['pie_charts'],
        bars=graphs['bar_charts'],
        lines=graphs['line_charts'],
        user=current_user)


@route('/query_builder', methods=['GET', 'POST'])
@login_required
def query_builder():
    # type: () -> text_type
    """Generates web pivot table based on Olapy star_schema_DataFrame.

    :return: pivottable.js
    """
    cubes_path = os.path.join(current_app.instance_path, 'olapy-data', 'cubes')

    config = ConfigParser(cube_path=cubes_path)

    executer = MdxEngine(
        cube_name=config.get_cubes_names(client_type='web').keys()[0],
        cubes_path=cubes_path,
        client_type='web')

    df = executer.get_star_schema_dataframe()
    if not df.empty:
        pivot_ui(
            df,
            outfile_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'templates',
                'pivottablejs.html'),
            height="100%")

    return render_template('query_builder.html', user=current_user)


@route('/qbuilder')
@login_required
def qbuilder():
    # type: () -> text_type
    """
    Show pivottablejs.html (generated with :func:`query_builder` ) as an iframe
    :return: pivottablejs.html
    """
    return render_template('pivottablejs.html')
