from __future__ import absolute_import, division, print_function

import itertools
import os
from io import BytesIO
from itertools import groupby
from operator import itemgetter

import pandas as pd
from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required, login_user, logout_user
from olapy.core.mdx.executor.execute import MdxEngine
from olapy.core.mdx.tools.config_file_parser import ConfigParser
from pandas import DataFrame, Series
from treelib import Tree
from treelib.tree import DuplicatedNodeIdError

from web.pivottable import pivot_ui

from web import app, login_manager
from web.logger import Logs
from web.stats_utils import Graphs
from .forms import LoginForm, QueryForm
from .models import User


class Nod:
    """Class for maintaining dimensions hierarchies."""

    # in pandas there is a problem with conversion multiindex dataframe to json
    # to solve the export to excel problem we used a global variable
    # TODO remove this , ( right know this is just a demo with sales cube )
    CUBE = 'sales'
    frame = pd.DataFrame()
    ex = MdxEngine(CUBE)

    log = Logs('all')
    log_users = Logs('users')
    log_mdx = Logs('mdx')

    def __init__(self, text, id, parent):
        self.text = text
        self.id = id
        self.parent = parent

    def __str__(self):
        return '''
        {"id": "''' + str(self.id) + '''" ,"parent": "''' + str(
            self.parent) + '''","text": "''' + str(self.text) + '''"}'''


def generate_tree_levels():
    """
    Build table's levels to use them in the page's TreeView.

    :return: dict of levels
    """
    levels = {}
    for t in Nod.ex.tables_names:
        if t != Nod.ex.facts:
            df = Nod.ex.tables_loaded[t]
            tree = Tree()
            tree.create_node(t, t, data=t)

            for c in df.columns[1:]:
                for k, v in groupby(
                        sorted((df.groupby(
                            list(df.columns.values[
                                0:df.columns.get_loc(c) + 1])).groups).keys()),
                        key=itemgetter(*range(0, df.columns.get_loc(c)))):

                    if type(k) not in [list, tuple]:
                        tree.create_node(
                            str(k), str(k), parent=t, data=str(k))  # root node
                    for i in v:
                        if isinstance(i, tuple):
                            try:
                                tree.create_node(
                                    str(".".join(
                                        ["[" + str(x) + "]" for x in i])),
                                    str(i[-1]),
                                    parent=str(k[-1])
                                    if type(k) in [list, tuple] else str(k),
                                    data=str(i[-1]))
                            except DuplicatedNodeIdError:
                                pass
            levels.update({t: tree})
    return levels


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
    return redirect('/execute')
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
            Nod.log.write_log('connected as ' + str(current_user.username))
            Nod.log_users.write_log('connected as ' +
                                    str(current_user.username))
            return redirect(
                request.args.get('next') or
                url_for('execute', user=current_user))
        flash('incorrect username or password')
    return render_template('login.html', form=form, user=current_user)


@app.route('/logout')
def logout():
    Nod.log.write_log('logout as ' + str(current_user.username))
    Nod.log_users.write_log('logout as ' + str(current_user.username))
    logout_user()
    return redirect(url_for('login'))


@app.route('/execute', methods=['GET', 'POST'])
@login_required
def execute():
    form = QueryForm()

    # if we have a slow page load we have to com the line below
    lvls = generate_tree_levels()
    nods = {}
    for t in Nod.ex.tables_names:
        if t != Nod.ex.facts:
            l_nods = []
            for node in lvls[t].expand_tree(mode=Tree.DEPTH):
                if lvls[t][node].fpointer:
                    for x in lvls[t][node].fpointer:
                        if node == t:
                            parent = "#"
                        else:
                            parent = node
                        nod = Nod(x, x, parent)
                        l_nods.append(nod)
            nods.update({t: l_nods})

    if form.validate_on_submit():
        query = form.mdx.data
        Nod.log.write_log('Query : ' + str(query))
        Nod.log_mdx.write_log('Query : ' + str(query))
        Nod.ex.mdx_query = query
        rslt = Nod.ex.execute_mdx()['result']
        Nod.log.write_log('Query result :  ' + str(rslt))
        Nod.log_mdx.write_log('Query result :  ' + str(rslt))

        # we used a global variable which will contain the dataframe execution result
        # because pandas current version has problem converting multiindex
        # dataframe to json format
        Nod.frame = rslt

        if isinstance(rslt, DataFrame):
            t_rslt = rslt.to_html(
                classes=['table table-bordered table-hover table-striped'])
        elif isinstance(rslt, Series):
            t_rslt = rslt.to_frame().to_html(
                classes=['table table-bordered table-hover table-striped'])

        return render_template(
            'execute_query.html',
            user=current_user,
            form=form,
            t_result=t_rslt,
            tables=Nod.ex.tables_loaded,
            cube=Nod.CUBE,
            measures=Nod.ex.measures,
            hierarchies=nods)

    return render_template(
        'execute_query.html',
        user=current_user,
        form=form,
        tables=Nod.ex.tables_loaded,
        cube=Nod.CUBE,
        measures=Nod.ex.measures,
        hierarchies=nods)


@app.route('/export', methods=['GET', 'POST'])
@login_required
def export():
    if not Nod.frame.empty:
        df = pd.DataFrame(Nod.frame)
        Nod.log.write_log('Export :  ' + str(df))
        Nod.log_mdx.write_log('Export :  ' + str(df))
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]
        format = workbook.add_format()
        format.set_bg_color('#eeeeee')
        worksheet.set_column(0, 9, 28)
        # the writer has done its job
        writer.close()
        # go back to the beginning of the stream
        output.seek(0)
        # finally return the file
        return send_file(
            output, attachment_filename="output.xlsx", as_attachment=True)

    return redirect('/execute')


@app.route('/export/<type>', methods=['GET', 'POST'])
@login_required
def export_file(type):
    if Nod.log.root_path:
        return send_file(
            os.path.join(Nod.log.root_path, type + '.log'), as_attachment=True)
    return redirect('/execute')


@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    ex = MdxEngine(Nod.CUBE)
    graph = Graphs()

    columns = list(
        itertools.chain.from_iterable([[column for column in df.columns]
                                       for table_name, df in ex.tables_loaded.
                                       items() if table_name != ex.facts]))
    columns.append(ex.measures[0])

    temp_rslt = ex.load_star_schema_dataframe[columns].head(200)
    # so we can export it to excel
    Nod.frame = ex.load_star_schema_dataframe[columns]
    graph = graph.generate_graphes(temp_rslt)

    return render_template(
        'stats.html',
        user=current_user,
        table_result=temp_rslt.to_html(classes=[
            'table table-bordered table-hover table-striped display'
        ]),
        graphe=graph,
        ids=graph['ids'])


@app.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    ex = MdxEngine('mpr')
    star_df = ex.get_star_schema_dataframe('web')
    # temp_rslt = temp_rslt[ ['budget_total','subvention_totale']]
    # temp_rslt = temp_rslt.groupby(['Pole leader', 'Type', 'Status', 'labelized', 'financed']).sum()[
    #     ['budget_total', 'subvention_totale']]
    # OU BIEN

    import numpy as np
    # margins = True ( prob )
    conf = ConfigParser(ex.cube_path)


    dash = conf.construct_web_dashboard()[0]

    temp_rslt = pd.pivot_table(star_df,
                               values=ex.measures,
                               index=dash.global_table['columns'],
                               columns=dash.global_table['rows'], aggfunc=np.sum)

    graph = Graphs()
    # graph = graph.generate_graphes(ex.get_star_schema_dataframe('web')[['Status','budget_total']])

    # star['Status'].value_counts().to_frame()

    # for pie_chart in conf.construct_web_dashboard()[0].pie_charts:
    #     print(pie_chart)

    dfs = []

    for pie_chart in conf.construct_web_dashboard()[0].pie_charts:
        df = star_df[pie_chart].value_counts().to_frame().reset_index()
        df.name = pie_chart
        dfs.append(df)
    graph = graph.generate_pie_graphes(dfs)

    dfs2 = []
    graph2 = Graphs()
    for bar_chart in conf.construct_web_dashboard()[0].bar_chats:
        df = star_df[[bar_chart] + ex.measures].groupby([bar_chart]).sum().reset_index()
        df.name = bar_chart
        dfs2.append(df)


    graph2 = graph2.generate_bar_graphes(dfs2)

    dfs3 = []
    graph3 = Graphs()
    for column_name,columns_attributs in conf.construct_web_dashboard()[0].line_charts.items():
        df = star_df[[column_name] + ex.measures].groupby([column_name]).sum().reset_index()
        df.name = column_name
        if columns_attributs is not 'ALL':
            df = df[df[column_name].isin(columns_attributs)]
        dfs3.append(df)

        # df2 = star[['annee_immatriculation', 'budget_total']].groupby(['annee_immatriculation']).sum().reset_index()
        # df2[['annee_immatriculation']] = df2[['annee_immatriculation']].astype(np.int)

        # df2[df2['annee_immatriculation'].isin([1954, 2000])]

    graph3 = graph3.generate_line_graphes(dfs3)


    return render_template(
        'dash.html',
        table_result=temp_rslt.to_html(classes=[
            'table m-0 table-primary table-colored table-bordered table-hover table-striped display'
        ]),
        graphe=graph,
        ids=graph['ids'],
        graphe2=graph2,
        ids2=graph2['ids'],
        graphe3=graph3,
        ids3=graph3['ids'],
        user=current_user)


@app.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    return render_template('logs.html', user=current_user)


@app.route('/query_builder', methods=['GET', 'POST'])
@login_required
def query_builder():
    # df = Nod.ex.load_star_schema_dataframe
    # if not df.empty:

    executer = MdxEngine('mpr')
    df = executer.get_star_schema_dataframe(client_type='web')

    if not df.empty:
        pivot_ui(
            df,
            outfile_path="web/templates/pivottablejs.html",
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
