from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SubmissionForm(FlaskForm):
    content = TextAreaField('Your Answer', validators=[DataRequired(message='Answer cannot be empty.'),
                                                       Length(min=10, max=1000, message='Answer must be between 10 and 1000 characters.')])
    submit = SubmitField('Submit Assignment')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Feedback')