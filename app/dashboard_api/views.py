# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from flask import Blueprint, jsonify
# from flask import current_app
from flask_login import login_required, current_user

from app.models import User, Dashboard

DASH_API = Blueprint('dash_api', __name__, template_folder='templates')
dash_api = DASH_API.route


@dash_api('dashboards')
@login_required
def get_dashboards():
    user_dashboards = Dashboard.query.filter(User.id == current_user.id).all()
    return jsonify([dashboard.name for dashboard in user_dashboards])
