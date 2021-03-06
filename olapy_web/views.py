from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers import Response

from .extensions import login_manager
from .forms import LoginForm
from .models import User

blueprint = Blueprint("main", __name__)
route = blueprint.route


@login_manager.user_loader
def load_user(userid: str) -> User:
    """Load user with specific id."""
    return User.query.get(int(userid))


@route("/index")
@route("/")
@login_required
def index() -> str:
    return render_template("index.html", user=current_user)


@route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    """Login user."""
    form = LoginForm()
    if len(form.errors) > 0:
        flash(form.errors)
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            # next to hold the the page that the user tries to visite

            next_url = request.args.get("next") or url_for("main.index")
            return redirect(next_url)

        flash("incorrect username or password")

    return render_template("login.html", form=form, user=current_user)


@route("/logout")
def logout() -> Response:
    """Logout user."""
    logout_user()
    return redirect(url_for("main.login"))
