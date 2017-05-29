from __future__ import absolute_import, division, print_function



from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from olapy.core.mdx.executor.execute import MdxEngine
from olapy.core.mdx.tools.config_file_parser import ConfigParser

from .pivottable import pivot_ui

from . import app, login_manager
from .stats_utils import GraphsGen
from .forms import LoginForm
from .models import User


@login_manager.user_loader
def load_user(userid):
    """
    Load user with specific id.

    :param userid: user id
    :return: user
    """
    return User.query.get(int(userid))


@app.route('/index')
@app.route('/')
def index():
    return redirect('/dashboard')
    # return render_template('execute_query.html',user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if len(form.errors) > 0:
        flash(form.errors)
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            # next to hold the the page that the user tries to visite

            return redirect(
                request.args.get('next') or
                url_for('dashboard', user=current_user))
        flash('incorrect username or password')
    return render_template('login.html', form=form, user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def _construct_charts(dashboard, executer):
    graph_gen = GraphsGen()
    graphes = {}
    star_dataframe = executer.get_star_schema_dataframe()

    for chart_type, chart_attributs in dashboard.__dict__.items():
        all_dataframes = []
        tables_names = []
        total = {}
        if chart_type == 'pie_charts':
            for chart_table_column in chart_attributs:
                total[chart_table_column] = star_dataframe[chart_table_column].value_counts().sum()
                df = star_dataframe[chart_table_column].value_counts().to_frame().reset_index()
                all_dataframes.append(df)
                tables_names.append(chart_table_column)

            graphes['pie_charts'] = {'graphes': graph_gen.generate_pie_graphes(all_dataframes),
                                     'totals': total,
                                     'tables_names': tables_names}

        elif chart_type == 'bar_charts':
            for measure in executer.measures:
                total[measure] = star_dataframe[measure].sum()
            for chart_table_column in chart_attributs:
                df = star_dataframe[[chart_table_column] + executer.measures].groupby(
                    [chart_table_column]).sum().reset_index()
                all_dataframes.append(df)
                tables_names.append(chart_table_column)

            graphes['bar_charts'] = {'graphes': graph_gen.generate_bar_graphes(all_dataframes),
                                     'totals': total,
                                     'tables_names': tables_names}


        elif chart_type == 'line_charts':
            for measure in executer.measures:
                total[measure] = star_dataframe[measure].sum()

            for column_name, columns_attributs in chart_attributs.items():
                df = star_dataframe[[column_name] + executer.measures].groupby([column_name]).sum().reset_index()

                # filter columns to show
                if columns_attributs is not 'ALL':
                    df = df[df[column_name].isin(columns_attributs)]

                tables_names.append(column_name)
                all_dataframes.append(df)

            graphes['line_charts'] = {'graphes': graph_gen.generate_line_graphes(all_dataframes),
                                      'totals': total,
                                      'tables_names': tables_names}

    return graphes


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    import pandas as pd
    import numpy as np
    # TODO use plotly dashboard !!!

    config = ConfigParser()
    executer = MdxEngine(config.get_cubes_names(client_type='web').keys()[0], client_type='web')
    dashboard = config.construct_web_dashboard()[0]
    graphes = _construct_charts(dashboard, executer)

    # todo margins = True ( prob )
    pivote_table_df = pd.pivot_table(executer.get_star_schema_dataframe(),
                                     values=executer.measures,
                                     index=dashboard.global_table['columns'],
                                     columns=dashboard.global_table['rows'], aggfunc=np.sum)

    return render_template(
        'dashboard.html',
        table_result=pivote_table_df.to_html(classes=[
            'table m-0 table-primary table-colored table-bordered table-hover table-striped display'
        ]),
        pies=graphes['pie_charts'],
        bars=graphes['bar_charts'],
        lines=graphes['line_charts'],
        user=current_user)


@app.route('/query_builder', methods=['GET', 'POST'])
@login_required
def query_builder():
    # df = Nod.ex.load_star_schema_dataframe
    # if not df.empty:
    config = ConfigParser()
    executer = MdxEngine(config.get_cubes_names(client_type='web').keys()[0], client_type='web')
    df = executer.get_star_schema_dataframe()
    import os
    if not df.empty:
        pivot_ui(
            df,
            outfile_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates','pivottablejs.html'),
            height="100%")

    return render_template('query_builder.html', user=current_user)


@app.route('/qbuilder', methods=['GET'])
@login_required
def qbuilder():
    return render_template('pivottablejs.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
