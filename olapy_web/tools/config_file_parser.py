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
        """
        Parse olapy-web config web file.

        Config file used if you want to show only some measures, dimensions,
        columns... in excel

        Config file should be under '~/olapy-data/cubes/web-cubes-config.xml'

         <cubes>
               <cube>
                  <!-- cube name => db name -->
                  <name>mpr</name>

                  <!-- source : postgres | csv -->
                  <source>postgres</source>

                  <!-- star building customized star schema -->
                  <facts>
                     <!-- facts table name -->
                     <table_name>projet</table_name>

                     <keys>
                        <!-- ref = table_name.column  -->
                        <column_name ref="vocabulary_crm_status.id">status_id</column_name>
                        <column_name ref="vocabulary_crm_pole_leader.id">pole_leader_id</column_name>
                        <column_name ref="contact.id">contact_id</column_name>
                        <column_name ref="compte.id">compte_porteur_id</column_name>
                        <column_name ref="vocabulary_crm_aap_type.id">aap_name_id</column_name>
                     </keys>

                     <!-- specify measures explicitly -->
                     <measures>
                        <!-- by default, all number type columns in facts table, or you can specify them here -->
                        <name>budget_total</name>
                        <name>subvention_totale</name>
                        <name>duree_projet</name>
                     </measures>

                     <!-- additional columns to keep other than measures and ids -->
                     <columns>etat,aap,axes_de_developpement</columns>
                  </facts>

                  <!-- end building customized star schema -->
                  <tables>
                     <!-- Table name -->
                     <table name="vocabulary_crm_status">

                        <!-- Columns to keep (INCLUDING id)-->
                        <!-- They must be seperated with comma ',' -->
                        <columns>id,label</columns>

                        <!-- Change insignificant table columns names -->
                        <!-- {IMPORTANT} Renaming COMMUN columns between dimensions and other columns if you want, other than ids column -->
                        <new_name old_column_name="label">Status</new_name>
                     </table>

                     <table name="contact">
                        <columns>id,nom,prenom,fonction</columns>
                        <new_name old_column_name="fonction">Contact Fonction</new_name>
                     </table>
                  </tables>

                  <!-- Dashboards -->
                  <Dashboards>
                     <Dashboard>
                        <Global_table>
                           <!-- IMPORTANT !! columns and rows names must be specified as above with their new names -->
                           <!-- EXAMPLE <new_name old_column_name="label">Pole leader</new_name>, you put Pole leader -->
                           <!-- marches,axes_de_developpement,statut_pour_book are columns from facts table  -->
                           <columns>marches,axes_de_developpement</columns>
                           <rows>statut_pour_book</rows>
                        </Global_table>

                        <!-- Contact Fonction,Type Organisation columns name from different tables (with ther new names) -->
                        <PieCharts>Contact Fonction,Type Organisation</PieCharts>

                        <!-- TODO BarCharts with Stacked Bar Chart -->
                        <BarCharts>Avis</BarCharts>

                        <!-- Preferably with time/date (or sequenced) tables-->
                        <LineCharts>
                           <table>
                              <!-- date_debut_envisagee a column from facts table  -->
                              <name>date_debut_envisagee</name>
                              <!-- if not specified, then all columns attributs -->
                              <!--<columns>1945,2000,2006,2015</columns> -->
                           </table>
                        </LineCharts>
                     </Dashboard>
                  </Dashboards>
                <!-- END Dashboards -->
               </cube>
        </cubes>

        :return:
        """
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
