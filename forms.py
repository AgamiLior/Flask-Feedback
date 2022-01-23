from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """ Registration form """
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("Firstname", validators=[InputRequired()])
    last_name = StringField("Lastname", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username",validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password")

class UserForm(FlaskForm):
    """This form is just blank form."""
    
class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title",validators=[InputRequired(), Length(max=100)])
    content = StringField("Content",validators=[InputRequired()])
