from __future__ import absolute_import, division, print_function, unicode_literals

import os

import yaml


# TEMPORARY JUST FOR QUERY BUILDER
class ConfigParser:
    def __init__(self, web_config_file_name=None):

        if web_config_file_name:
            self.web_config_file_name = web_config_file_name
        else:
            self.web_config_file_name = 'web_cube_config.yml'

    def config_file_exists(self):
        """
        Check whether the config file exists or not.
        :param client_type: excel config file or web
        :return: True | False
        """

        return os.path.isfile(self.web_config_file_name)

    def construct_web_dashboard(self):
        """
        Parse olapy-web config web file.
        Config file used if you want to show only some measures, dimensions,
        columns... in excel
        Config file should be under '~/olapy-data/cubes/web-cubes-config.xml'
        name : foodmart_with_config            # csv folder name or db name
        source : csv                           # csv | postgres | mysql ...
        facts :                                # facts table name
          table_name : food_facts
          keys:                                # primary keys
            columns_names :
              - product_id
              - warehouse_id
              - store_id
            refs :                             # keys refs (example : product_id ref to column id from table Product...)
              - Product.id
              - Warehouse.id
              - Store.id
          measures :                  # by default, all number type columns in facts table, or you can specify them here
            - units_ordered
            - units_shipped
            - supply_time
        tables :                               #  additional columns to keep other than measures and ids columns :
          - table :
              name : Product
              columns : id,brand_name,product_name
              new_names :
                product_name : Product_Name
          - table :
              name : Store
              columns : id,store_type,store_name,store_city
          - table :
              name : Warehouse
              columns : id,warehouse_name,warehouse_city,warehouse_country
        # IMPORTANT !! columns and rows names must be specified as above with their new names
        # EXAMPLE <new_name old_column_name="label">Pole leader</new_name>, you put Pole leader
        # marches,axes_de_developpement,statut_pour_book are columns from facts table
        Dashboard :
          Global_table:
            columns :
              - warehouse_name
              - warehouse_country
              - store_type
              - store_name
              - brand_name
            rows :
              - store_city
          PieCharts :
            - store_city
            - store_type
            - warehouse_city
          BarCharts :
            - warehouse_country
        #  LineCharts :                                             # Preferably with time/date (or sequenced) tables
        #    table : Year
        #    columns :
        #      - 2010
        #      - 2011
        :return: dashboard (dict)
        """
        with open(self.web_config_file_name) as config_file:
            config = yaml.load(config_file)

        return {
            'global_table': config['Dashboard']['Global_table'],
            'PieCharts': config['Dashboard']['PieCharts'],
            'BarCharts': config['Dashboard']['BarCharts'],
            'LineCharts': {
                config['Dashboard']['LineCharts']['table']:
                    config['Dashboard']['LineCharts']['columns'] if
                    'columns' in config['Dashboard']['LineCharts'] else 'ALL'
            } if 'LineCharts' in config['Dashboard'] else {}
        }

    def construct_cubes(self):
        """
        Construct parser cube obj (which can ben passed to MdxEngine) for web
        :return: Cube obj
        """
        if not self.config_file_exists():
            raise ValueError("Config file doesn't exist")
        with open(self.web_config_file_name) as config_file:
            config = yaml.load(config_file)

            if 'facts' in config:
                facts = {
                    'table_name': config['facts']['table_name'],
                    'keys': dict(
                        zip(config['facts']['keys']['columns_names'],
                            config['facts']['keys']['refs'])),
                    'measures': config['facts']['measures'],
                    'columns': config['facts']['columns']
                    if 'columns' in config['facts'] else '',
                }

            else:
                facts = []

            if 'tables' in config:
                tables = [
                    {
                        'name': table['table']['name'],
                        'columns': table['table']['columns'],
                        'new_names': {new_col
                                      for new_col in table['table']['new_names']} if 'new_names' in table[
                            'table'] else {},
                    } for table in config['tables']
                ]
            else:
                tables = []

        return {
            'name': config['name'],
            'source': config['source'],
            'facts': facts,
            'tables': tables
        }
