# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from flask import Blueprint, jsonify, request
# from flask import current_app
from flask_login import login_required, current_user

from app.extensions import db
from app.models import User, Dashboard

DASH_API = Blueprint('dashboard_api', __name__, template_folder='templates')
dash_api = DASH_API.route


@dash_api('save', methods=['POST'])
@login_required
def save_dashboard():
    request_data = request.get_json()
    user_dashboard = User.query.filter(User.id == current_user.id).first().dashboards
    if user_dashboard:
        # update dashboard
        user_dashboard.name = request_data['dashboardName']
        user_dashboard.content = request_data['dashboardContent']
    else:
        # add new cube
        cube = Dashboard(name=request_data['dashboardName'],
                         content=request_data['dashboardContent'],
                         user_id=current_user.id
                         )
        db.session.add(cube)
    db.session.commit()
    return jsonify({'success': True}), 200


@dash_api('all')
@login_required
def all_dashboard():
    all_dashboards = User.query.filter(User.id == current_user.id).first().dashboards
    return jsonify([dashboard.name for dashboard in all_dashboards])
