from __future__ import absolute_import, division, print_function
# unicode_literals causes some problems with plotly
# , unicode_literals

import attr
from typing import Dict
import pandas as pd
import json
import plotly
import plotly.graph_objs as go


@attr.s
class Facts(object):
    """Facts class used to encapsulate config file attributes."""

    table_name = attr.ib()
    keys = attr.ib()
    measures = attr.ib()
    columns = attr.ib()


class Chart(object):

    def __init__(self, executor, columns_names):
        self.executor = executor
        self.columns_names = columns_names

    def _gen_tables_names(self):
        return [column_name for column_name in self.columns_names]

    def _generate_graphs(self):
        pass

    def _gen_columns_sum(self):
        pass

    def _get_pattern(self):
        return '_graph-{}'

    def _gen_graph_ids_json(self):
        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        graphs = self._generate_graphs()
        ids = [self._get_pattern().format(i) for i, _ in enumerate(graphs)]
        graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
        # TODO use this
        # div = offplot.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
        return {'ids': ids, 'graph_json': graph_json}

    def gen_graphs(self):
        return {
            'graphs': self._gen_graph_ids_json(),
            'totals': self._gen_columns_sum(),
            'tables_names': self._gen_tables_names()
        }


class PieChart(Chart):
    Chart.ids_patter = 'pie_graph-{}'

    def generate_pie_graph(self, dataframe):
        # type: (pd.DataFrame) -> Dict
        """Generate graphs for a list of Pandas DataFrames.

        If you want to add graphs, you have to do it in this function.

        :param dataframes: a list of DataFrames

        :return: dict of ids as keys and json graphs as values
        """
        x = []
        y = []
        for idx, row in dataframe.iterrows():
            # x_pie to avoid the long words
            x.append(row[-2])
            y.append(row[-1])

        y = pd.Series(y)
        # https: // plot.ly / python / reference
        # Create the Plotly Data Structure
        # go.Scatter
        # go.Bar

        return dict(data=[{
            # 'title' : dataframe.name,
            'labels': x,
            'values': y,
            'type': 'pie',
            'visible': True,
            'showlegend': True,
            # 'show_link' : False,
            # # 'link' : False,
            # 'colorscale' : 'blues',
            # 'textposition' : 'outside',
            # 'textinfo' : 'value+percent',
            'pull': .2,
            'hole': .2
        }])

    def _gen_columns_sum(self):
        total = {}
        for column_name in self.columns_names:
            total[column_name] = self.executor.star_schema_dataframe[column_name].value_counts().sum()
        return total

    def _gen_df_rows_occurrences(self):
        all_dataframes = []
        for column_name in self.columns_names:
            df = self.executor.star_schema_dataframe[column_name].value_counts().to_frame().reset_index()
            all_dataframes.append(df)
        return all_dataframes

    def _generate_graphs(self):
        return [self.generate_pie_graph(df) for df in self._gen_df_rows_occurrences()]

    def _get_pattern(self):
        return 'pie_graph-{}'


class BarChart(Chart):
    # def __init__(self, *args, **kwargs):
    Chart.ids_patter = 'bar_graph-{}'

    # super(Chart, self).__init__()

    def generate_bar_graph(self, dataframe):
        # type: (pd.DataFrame) -> Dict
        """Generate graphs for a pandas DataFrame.

        If you want to add graphs, you have to do it in this function.

        :param dataframes: a list of DataFrames

        :return: dict of ids as keys and json graphs as values
        """
        traces = []
        for measure in dataframe[dataframe.columns[1:]]:
            x = list(dataframe[dataframe.columns[0]])
            y = list(dataframe[measure])
            # https: // plot.ly / python / reference
            # Create the Plotly Data Structure
            # go.Scatter
            # go.Bar
            traces.append(go.Bar(x=x, y=y, name=measure))

        return dict(
            data=traces,
            show_link=False,
            layout=go.Layout(barmode='group'))

    def _gen_columns_sum(self):
        total = {}
        for measure in self.executor.measures:
            total[measure] = self.executor.star_schema_dataframe[measure].sum()
        return total

    def _gen_df_rows_occurrences(self):
        all_dataframes = []
        for column_name in self.columns_names:
            df = self.executor.star_schema_dataframe[[column_name] +
                                                     self.executor.measures].groupby(
                [column_name]).sum().reset_index()
            all_dataframes.append(df)
        return all_dataframes

    def _generate_graphs(self):
        return [self.generate_bar_graph(df) for df in self._gen_df_rows_occurrences()]

    def _get_pattern(self):
        return 'bar_graph-{}'


class LineChart(Chart):
    Chart.ids_patter = 'line_graph-{}'

    def generate_line_graph(self, dataframe):
        # type: (pd.DataFrame) -> Dict
        """Generate graphs for a list of Pandas DataFrames.

        If you want to add graphs, you have to do it in this function.

        :param dataframes: a list of DataFrames

        :return: dict of ids as keys and json graphs as values
        """

        traces = []
        for measure in dataframe[dataframe.columns[1:]]:
            x = list(dataframe[dataframe.columns[0]])
            y = list(dataframe[measure])
            # https: // plot.ly / python / reference
            # Create the Plotly Data Structure
            # go.Scatter
            # go.Bar
            traces.append(
                go.Scatter(x=x, y=y, name=measure, mode='lines+markers'))

        return dict(data=traces)

    def _gen_columns_sum(self):
        total = {}
        for measure in self.executor.measures:
            total[measure] = self.executor.star_schema_dataframe[measure].sum()
        return total

    def _gen_df_rows_occurrences(self):
        all_dataframes = []
        for column_name, columns_attributs in self.columns_names.items():
            df = self.executor.star_schema_dataframe[[column_name] + self.executor.measures].groupby(
                [column_name]).sum().reset_index()

            # filter columns to show
            if columns_attributs is not 'ALL':
                df = df[df[column_name].isin(columns_attributs)]

            all_dataframes.append(df)
        return all_dataframes

    def _generate_graphs(self):
        return [self.generate_line_graph(df) for df in self._gen_df_rows_occurrences()]

    def _get_pattern(self):
        return 'line_graph-{}'
