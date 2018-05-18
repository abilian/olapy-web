=====================
 Customize Olapy-web
=====================

After Running Olapy-web for the first time, Olapy-core dependencies
will be installed on the machine and with it some cubes demos and
configuration files. You can check them under::

    ~/olapy-data # for mac/linux

    C:\\User\\{USER_NAME}\\olapy-data # for windows

One of the configurations files that interest us for Olapy-web is ``web_cube_config.xml``::


    ~/olapy-data/cubes/web_cube_config.xml # for mac/linux

    C:\\User\\{USER_NAME}\\olapy-data\cubes\web_cube_config.xml # for windows


Star schema construction
========================

The Default web_cube_config works with a sales cube which follows the :mod:`OLAPY CUBES RULES <OLAPY CUBES RULES>`::

    <cubes>
       <cube>

          <!-- cube name | db name -->
          <name>sales</name>
          <!-- source : csv | postgres | mysql| mssql | oracle -->
          <source>csv</source>

       </cube>
    </cubes>


So if you want to use your own cube to follow the :mod:`OLAPY CUBES RULES <OLAPY CUBES RULES>`, just replace the name and the source.

Star schema customization
=========================
if you want to customize the star schema construction follow :mod:`Cube customization <Cube customization>`, the same principal, just some tags will be replaced and others added.

-   **<columns> tag**

A new tag must be added, <columns> under <facts>::

    <facts>
        ...

        <columns> ... </columns>
    </facts>

this <columns> tag contains additional columns that exist on the facts table and which are neither ids nor measures. Column names must be separated by a comma::

    <columns>Column1,Column2...</columns>

if you don't have any additional columns, just use an empty <columns> tag like this::

    <columns></columns>

**Don't remove columns tag in any case**.

-   **<tables> tag**

The <tables> tag came to replace <dimensions>. In this part you specify which column to keep for each table.

For example let's have "product" table with the following columns: ``id``, ``brand_name``, ``product_name``, ``product_type``, ``product_category``... and you want to use only some of those columns, so just put them in the <columns> tag like this::

    <tables>

         <!-- Table name -->
         <table name="Product">
            <!-- Columns to keep (INCLUDING id)-->
            <!-- They must be seperated with comma ',' -->
            <columns>id,brand_name,product_name</columns>
         </table>

         ... <!-- other tables -->

    </tables>

You can also change some columns names with the <new_name> tag: if you want to change ``brand_name`` to ``Name`` you can do something like this::

    <tables>

         <!-- Table name -->
         <table name="Product">
            <!-- Columns to keep (INCLUDING id)-->
            <!-- They must be seperated with comma ',' -->
            <columns>id,brand_name,product_name</columns>

             <!-- Change insignificant table columns names -->
             <!-- {IMPORTANT} Renaming COMMON columns between dimensions and other columns if you want, other than ids column -->

             <new_name old_column_name="product_name">Name</new_name>

         </table>

         ... <!-- other tables -->

    </tables>

Dashboard
=========

The second section that should exist in this file is the Dashboard section. It contains all the charts and tables you want to show and must be under the <cube> tag::

        <cubes>
            <cube>

                ....

                <Dashboards>
                    <Dashboard>

                        ... <!--  And here you put your charts and tables -->

                    </Dashboards>
                <Dashboard>

           </cube>
        </cubes>


PieCharts
---------

To add pie charts just add a <PieCarts> tag under <Dashboards> with the desired columns name like this::

    <PieCharts>Country,Licence,Continent</PieCharts>

A pie chart will be created for each column, so with the above example we get three.

BarCharts
---------

To add bar charts use <BarCharts>::

    <BarCharts>Licence,Continent</BarCharts>


Global table
------------

The Global table is the Star schema table itself. Add a <Global_table> tag under <Dashboards> and choose which columns to show::


    <Global_table>

       <columns>Continent,Country</columns>
       <rows>Licence,Year</rows>

    </Global_table>


.. note::

   If you rename a column in the :ref:`Star schema customization <Star schema customization>` you have to use the same name in dashboards.

**For a clearer example you can check**:

- the default web_cube_config.xml with sales cube (csv files under cubes/sales folder)

- the default web_cube_config2.xml with foodmart_with_config cube (csv files under cubes/foodmart_with_config folder)
