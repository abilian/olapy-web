from olapy.core.mdx.executor.execute import SUPPORTED_FILES, SUPPORTED_DATABASES, MdxEngine
from olapy.core.mdx.executor.execute_config_file import construct_web_star_schema_config_file
from olapy.core.mdx.executor.execute_csv_files import construct_star_schema_csv_files
from olapy.core.mdx.executor.execute_db import construct_star_schema_db


class CubeConstructor:


    def construct_star_schema_from_config(self, config_file_parser):
        """
        There is two different configuration, one for excel 'cubes-config.xml', \
        and the other for the web 'web_cube_config.xml' (if you want to use olapy-web), they are a bit different.
        :param config_file_parser: star schema Dataframe
        :return:
        """
        fusion = None
        for cubes in config_file_parser.construct_cubes():
            if cubes.source.upper() in SUPPORTED_FILES + SUPPORTED_DATABASES:
                    # todo clean!!!!!
                    if cubes.facts:
                        fusion = construct_web_star_schema_config_file(self, cubes)
                    # todo clean!!!!! # todo clean!!!!! # todo clean!!!!!
                    elif cubes.source.upper() in SUPPORTED_FILES and cubes.name in MdxEngine.csv_files_cubes:
                        fusion = construct_star_schema_csv_files(self)
                    elif cubes.source.upper() in SUPPORTED_DATABASES and cubes.name in MdxEngine.from_db_cubes:
                        fusion = construct_star_schema_db(self)
        return fusion
