from flask import jsonify, request

from olapy_web.extensions import db
from olapy_web.models import Chart, Dashboard

from . import route
from .util import get_current_user


@route("/dashboard/save", methods=["POST"])
def save_dashboard():
    request_data = request.get_json()
    user_dashboard = (
        get_current_user()
        .dashboards.filter(Dashboard.name == request_data["dashboardName"])
        .first()
    )
    if user_dashboard:
        # update dashboard
        user_dashboard.name = request_data["dashboardName"]
        user_dashboard.chart.used_charts = request_data["usedCharts"]
        user_dashboard.chart.charts_layout = request_data["layout"]
        user_dashboard.chart.charts_data = request_data["chartData"]
    else:
        # add new cube
        chart = Chart(
            used_charts=request_data["usedCharts"],
            charts_layout=request_data["layout"],
            charts_data=request_data["chartData"],
        )
        dashboard = Dashboard(
            name=request_data["dashboardName"],
            user_id=get_current_user().id,
            chart=chart,
        )
        db.session.add(dashboard)
    db.session.commit()
    return jsonify({"success": True}), 200


@route("/dashboard/all")
def all_dashboard():
    all_dashboards = get_current_user().dashboards
    return jsonify([dashboard.name for dashboard in all_dashboards])


@route("/dashboard/<dashboard_name>")
def get_dashboard(dashboard_name):
    dashboard = (
        get_current_user().dashboards.filter(Dashboard.name == dashboard_name).first()
    )
    return jsonify(
        {
            "name": dashboard.name,
            "used_charts": dashboard.chart.used_charts,
            "charts_layout": dashboard.chart.charts_layout,
            "charts_data": dashboard.chart.charts_data,
        }
    )


@route("/dashboard/delete", methods=["POST"])
def delete_dashboard():
    request_data = request.get_json()
    obj = (
        get_current_user()
        .dashboards.filter(Dashboard.name == request_data["dashboardName"])
        .first()
    )
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"success": True}), 200
