from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
import sqlalchemy as sa
from app.models import User, Professor
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfessorLoginForm(FlaskForm):
    username = StringField('Professor Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StudentRegisterForm(FlaskForm):
    username = StringField('Student Username', validators=[DataRequired(), Length(min=2, max=20)])
    student_id = StringField('Student ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ProfessorRegisterForm(FlaskForm):
    username = StringField('Professor Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        professor = db.session.scalar(sa.select(Professor).where(Professor.username == username.data))
        if professor:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        professor = db.session.scalar(sa.select(Professor).where(Professor.email == email.data))
        if professor:
            raise ValidationError('That email is already in use. Please choose a different one.')
