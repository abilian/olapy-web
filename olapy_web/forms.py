from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Loging Form."""

    username = StringField(
        "Your username:", validators=[DataRequired(message="Please enter the Username")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Please enter the Password")]
    )
    remember_me = BooleanField("Remember Me ")
    submit = SubmitField("")
