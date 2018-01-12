from __future__ import absolute_import, division, print_function, unicode_literals

import os

from olapy_web.tools.models import Dashboard, Table, Cube, Facts
import yaml


class ConfigParser:
    def __init__(self, cubes_path, web_config_file_name='web_cube_config.yml'):
        self.cubes_path = cubes_path
        self.web_config_file_name = web_config_file_name

    def config_file_exists(self):
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
            config = yaml.load(config_file)

            try:
                return {config['name']: config['source']}
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
                    <!-- {IMPORTANT} Renaming COMMUN columns between dimensions and other columns if you want, \
                    other than ids column -->
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
            config = yaml.load(config_file)

        return [
            Dashboard(
                global_table=config['Dashboard']['Global_table'],
                PieCharts=config['Dashboard']['PieCharts'],
                BarCharts=config['Dashboard']['BarCharts'],
                LineCharts={config['Dashboard']['LineCharts']['table']:
                                config['Dashboard']['LineCharts']['columns'] if 'columns' in config['Dashboard']['LineCharts'] else 'ALL'}
            )
        ]

    def construct_cubes(self):
        """
        Construct parser cube obj (which can ben passed to MdxEngine) for web
        :return: Cube obj
        """
        if not self.config_file_exists():
            raise ValueError("Config file doesn't exist")
        with open(self.get_web_confile_file_path()) as config_file:
            config = yaml.load(config_file)

            if 'facts' in config:
                facts = [

                    Facts(

                        table_name=config['facts']['table_name'],
                        keys=dict(zip(config['facts']['keys']['columns_names'],
                                      config['facts']['keys']['refs'])
                                  ),
                        measures=config['facts']['measures'],
                        columns=config['facts']['columns'] if 'columns' in config['facts'] else '',
                    )
                ]
            else:
                facts = []

            if 'tables' in config:
                tables = [
                    Table(
                        name=table['name'],
                        columns=table['columns'],
                        new_names={
                            new_col for new_col in table['new_names']
                        },
                    ) for table in config['tables']

                ]
            else:
                tables = []

        return [
            Cube(
                name=config['name'],
                source=config['source'],
                facts=facts,
                tables=tables)
        ]
