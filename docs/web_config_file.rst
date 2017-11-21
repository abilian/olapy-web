Customize Olapy-web
-------------------

After Running Olapy-web for the first time, Olapy-core dependency will be installed on the machine and with it some cubes demos and configuration files, you can check then under::

    ~/olapy-data for mac/linux

    C:\\User\\{USER_NAME}\\olapy-data for windows

One of the configurations files that interest us for Olapy-web is *web_cube_config.xml*::


    ~/olapy-data/cubes/web_cube_config.xml for mac/linux

    C:\\User\\{USER_NAME}\\olapy-data\cubes\web_cube_config.xml for windows


Star schema construction
************************

The Default web_cube_config works with sales cube which follows :mod:`OLAPY CUBES RULES <OLAPY CUBES RULES>`::

    <cubes>
       <cube>

          <!-- cube name | db name -->
          <name>sales</name>
          <!-- source : csv | postgres | mysql| mssql | oracle -->
          <source>csv</source>

       </cube>
    </cubes>


So if you want to use your own cube which follows :mod:`OLAPY CUBES RULES <OLAPY CUBES RULES>`, just replace the name and source

Star schema customization
*************************
if you want to customize star schema construction follow :mod:`Cube customization <Cube customization>`, the same principal, just some tags will be replaced and others added.

-   **columns tag**

A new tag must be added, <columns> under <facts>::

    <facts>
        ...

        <columns> ... </columns>
    </facts>

this columns tag contains additional columns that exists on facts table and they are not neither ids or measures, columns name must be separated with comma::

    <columns>Column1,Column2...</columns>

if you don't have any additional columns, just put empty columns tag like this::

    <columns></columns>

**don't remove columns tag in any case**

-   **tables tag**

<tables> tag came to replace <dimensions>, in this part you specify which column to keep for each table,
for example table product with columns: id, brand_name, product_name, product_type, product_category... and you want to use only some of those columns, just put them in columns tag like this::

    <tables>

         <!-- Table name -->
         <table name="Product">
            <!-- Columns to keep (INCLUDING id)-->
            <!-- They must be seperated with comma ',' -->
            <columns>id,brand_name,product_name</columns>
         </table>

         ... <!-- other tables -->

    </tables>

you can also change some columns names with <new_name> tag, if you want to change *brand_name* column name to *Name* from above example you can do something like this::

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
*********

The second section that should exist in this file, is the Dashboard section which contains all charts and tables you want to show and must be under cube tag::

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
~~~~~~~~~

To add pie charts just add <PieCarts> tag under <Dashboards> with the desired columns name like this::

    <PieCharts>Country,Licence,Continent</PieCharts>

thus for each column a pie chart will be created, with above example, we have three pie charts

BarCharts
~~~~~~~~~

To add bar charts just add <BarCharts> tag under <Dashboards> with the desired columns name like this::

    <BarCharts>Licence,Continent</BarCharts>

thus for each column a bar chart will be created, with above example, we have two bar charts

Global table
~~~~~~~~~~~~~

The Global table is the Star schema table itself, add <Global_table> tag under <Dashboards> and choose which columns to show like this::


    <Global_table>

       <columns>Continent,Country</columns>
       <rows>Licence,Year</rows>

    </Global_table>


**IMPORTANT** : if you rename a columns in the:ref:`Star schema customization <Star schema customization>` you have to use the name names in dashboards

**For a clearer example you can check**:

-   default web_cube_config.xml with sales cube (csv files under cubes/sales folder)

-    default web_cube_config2.xml with foodmart_with_config cube (csv files under cubes/foodmart_with_config folder)