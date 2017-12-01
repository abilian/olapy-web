from __future__ import absolute_import, division, print_function, unicode_literals

import os

from olapy_web.tools.models import Dashboard, Table, Cube, Facts
from lxml import etree


class ConfigParser:
    def __init__(self, cubes_path, web_config_file_name='web_cube_config.xml'):
        self.cubes_path = cubes_path
        self.web_config_file_name = web_config_file_name

    def config_file_exist(self):
        """
        Check whether the config file exists or not.

        :param client_type: excel config file or web
        :return: True | False
        """

        return os.path.isfile(self.get_web_confile_file_path())

    def get_cubes_names(self):
        """Get all cubes names in the config file.

        :return: dict with dict name as key and cube source as value (csv | postgres | mysql | oracle | mssql)
        """
        file_path = self.get_web_confile_file_path()
        with open(file_path) as config_file:
            parser = etree.XMLParser()
            tree = etree.parse(config_file, parser)

            try:
                return {
                    cube.find('name').text: cube.find('source').text
                    for cube in tree.xpath('/cubes/cube')
                }
            except BaseException:  # pragma: no cover
                raise ValueError('missed name or source tags')

    def get_web_confile_file_path(self):
        return os.path.join(self.cubes_path, self.web_config_file_name)

    def construct_web_dashboard(self):
        with open(self.get_web_confile_file_path()) as config_file:
            parser = etree.XMLParser()
            tree = etree.parse(config_file, parser)

        return [
            Dashboard(
                global_table={
                    'columns':
                        dashboard.find('Global_table/columns').text.split(','),
                    'rows':
                        dashboard.find('Global_table/rows').text.split(','),
                },
                PieCharts=dashboard.find('PieCharts').text.split(','),
                BarCharts=dashboard.find('BarCharts').text.split(','),
                LineCharts={
                    table.find('name').text:
                        (table.find('columns').text.split(',')
                         if table.find('columns') is not None else 'ALL')
                    for table in dashboard.findall('LineCharts/table')
                }, )
            for dashboard in tree.xpath('/cubes/cube/Dashboards/Dashboard')
        ]

    def construct_cubes(self):
        """
        Construct parser cube obj (which can ben passed to MdxEngine) for web
        :return: Cube obj
        """
        if not self.config_file_exist():
            raise ValueError("Config file doesn't exist")
        with open(self.get_web_confile_file_path()) as config_file:
            parser = etree.XMLParser()
            tree = etree.parse(config_file, parser)
            facts = [
                Facts(
                    table_name=xml_facts.find('table_name').text,
                    keys={
                        key.text: key.attrib['ref']
                        for key in xml_facts.findall('keys/column_name')
                    },
                    measures=[
                        mes.text for mes in xml_facts.findall('measures/name')
                    ],
                    columns=xml_facts.find('columns').text.split(',') if xml_facts.find('columns') else '',
                )

                for xml_facts in tree.xpath('/cubes/cube/facts')
            ]

            tables = [
                Table(
                    name=xml_column.attrib['name'],
                    columns=xml_column.find('columns').text.split(','),
                    new_names={
                        new_col.attrib['old_column_name']: new_col.text
                        for new_col in xml_column.findall('new_name')
                    },
                ) for xml_column in tree.xpath('/cubes/cube/tables/table')
            ]

        return [
            Cube(
                name=xml_cube.find('name').text,
                source=xml_cube.find('source').text,
                facts=facts,
                tables=tables, ) for xml_cube in tree.xpath('/cubes/cube')
        ]
