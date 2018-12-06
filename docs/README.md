[OlaPy-Web](https://github.com/abilian/olapy-web) a web-based Online Analytical Processing (OLAP) exploration tool based on [OlaPy](https://github.com/abilian/olapy) 
that helps companies rethink business intelligence & data visualization.

It allows you to easily create powerful ad hoc reports and dashboards in minutes.


![Dashboard creation](https://raw.githubusercontent.com/abilian/olapy-web/master/docs/img/dash.gif)


![Pivottable](https://raw.githubusercontent.com/abilian/olapy-web/master/docs/img/pvt.gif)


Features:

* User Interface allowing for multiple views on-screen.
* Cube explorer providing Rollup and Drilldown operations with pivot table.
* Supports date filtering.
* Different types of charts and diagrams.
* View management, and dashboards saving.
* Easy Cube add.
* Secure user authentication. 


Installation
------------

First you need to clone the repository with:

    git clone https://github.com/abilian/olapy-web.git

To set up the application, run, ideally in a virtualenv:

    make develop

Run application:
----------------

1. Initialize application with:


    export FLASK_APP=manage.py


2. Initialize the db and some demos


    flask init 
    
    
3. run application:


    make run 
    
4. open your browser and go to [https://127.0.0.1:5000](https://127.0.0.1:5000)


**login: admin**

**password: admin**


*Links:*

[OlaPy-Web](https://github.com/abilian/olapy-web)

[OlaPy-Viz](https://github.com/abilian/olapy-web/tree/olapy-web2.0)

[OlaPy](https://github.com/abilian/olapy)