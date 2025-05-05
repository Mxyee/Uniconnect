from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField, DateTimeField
# from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
import sqlalchemy as sa
from app.models import User
from datetime import datetime, timedelta

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    submit = SubmitField('Choose')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def password_policy(form, field):
    message = """A password must be at least 8 characters long, and have an
                 uppercase and lowercase letter, and a digit"""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = False
    for ch in field.data:
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
    if not (flg_upper and flg_lower and flg_digit):
        raise ValidationError(message)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_policy])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(form, field):
        q = db.select(User).where(User.username==field.data)
        if db.session.scalar(q):
            raise ValidationError("Username already taken, please choose another")

    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError("Email address already taken, please choose another")


class CreateActivityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Date and Time', format='%Y-%m-%d %H:%M', default=lambda: (datetime.utcnow() + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0), validators=[DataRequired(message="Please enter a valid date in YYYY-MM-DD HH:MM format and it must be at least 7 days from today")])
    location = SelectField('Location', choices=[], validators=[DataRequired()])
    custom_location = StringField('Other Location', validators=[Optional(), Length(max=128)])
    submit = SubmitField('Create Activity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [
            ('', '--- Select a location ---'),
            # Red Zone
            ('R1', 'The Harding Building'),
            ('R2', 'Frankland Building'),
            ('R3', 'Hills Building'),
            ('R4', 'Aston Webb – Lapworth Museum'),
            ('R5', 'Aston Webb – B Block'),
            ('R6', 'Aston Webb – Great Hall'),
            ('R7', 'Aston Webb – Student Hub'),
            ('R8', 'Physics West'),
            ('R9', 'Physics East'),
            ('R10', 'Medical Physics'),
            ('R11', 'Ramsay Building'),
            ('R12', 'Barber Institute of Fine Arts'),
            ('R13', 'Watson Building'),
            ('R14', 'Ashley Building'),
            ('R15', 'Strathcona Building'),
            ('R16', 'Education Building'),
            ('R17', 'Jo G Smith Building'),
            ('R18', 'Muirhead Tower'),
            ('R19', 'University Centre'),
            ('R24', 'Staff House'),
            ('R26', 'Geography & Environmental Sciences'),
            ('R27', 'Biosciences Building'),
            ('R28', 'Murray Learning Centre'),
            ('R29', 'The Alan Walters Building'),
            ('R30', 'Collaborative Teaching Laboratory'),
            ('R31', 'Teaching and Learning Building'),
            ('R32', 'Metallurgy and Materials'),
            ('R33', 'FRI Building'),
            ('R34', 'Core'),
            ('R35', 'Molecular Sciences Building'),
            ('R36', 'Pritchatts Lodge 1'),
            ('R37', 'Pritchatts Lodge 2'),
            ('R38', 'Aston Webb Dome & Semi-Circle'),
            ('R39', 'Aston Webb Semi-Circle (West)'),
            ('R40', 'Sociology'),
            # Blue Zone
            ('B1', 'Medical School'),
            ('B2', 'Institute of Biomedical Research'),
            ('B3', 'Institute of Translational Medicine'),
            ('B4', 'Robert Aitken Institute'),
            ('B5', 'Dental Hospital'),
            ('B6', 'Wolfson Drive'),
            ('B7', 'Henry Wellcome Building for NMR Spectroscopy'),
            ('B8', 'Bioinnovation Hub'),
            ('B9', 'Health Research Bus'),
            # Orange Zone
            ('O1', 'The Guild of Students'),
            ('O2', 'St Francis Hall'),
            ('O3', 'University House'),
            ('O4', 'Ash House'),
            ('O5', 'Cedar House'),
            ('O6', 'Sport & Fitness'),
            ('O7', 'Elms House'),
            # Green Zone
            ('G1', '32 Pritchatts Road'),
            ('G2', '31 Pritchatts Road'),
            ('G3', 'European Research Institute'),
            ('G4', '3 Elms Road'),
            ('G5', 'Computer Centre'),
            ('G6', 'Metallurgy and Materials'),
            ('G7', 'IRC Net Shape Laboratory'),
            ('G8', 'Gisbert Kapp Building'),
            ('G9', '52 Pritchatts Road'),
            ('G10', '54 Pritchatts Road – The Institute of Advanced Studies'),
            ('G11', 'Maple House'),
            ('G12', 'Winterbourne House and Garden'),
            ('G13', 'Horton Grange'),
            ('G14', 'Garth House'),
            ('G15', 'Westmere'),
            ('G16', 'Lucas House'),
            ('G17', 'Peter Scott House'),
            ('G18', 'Priorsfield'),
            ('G19', 'Wolston Advanced Glasshouses'),
            ('G20', 'Park House'),
            ('G21', 'Gis Glashouses'),
            ('G22', 'Elms Day Nursery'),
            ('G23', 'Edgbaston Park Hotel and Conference Centre'),
            ('G24', 'Centre for Human Brain Health'),
            ('G25', 'Environmental Research Facility'),
            ('G26', 'Plasma Furnace'),
            ('G27', 'GMS Glasshouses'),
            # Yellow Zone
            ('Y1', 'The Old Gym'),
            ('Y2', 'Haworth Building'),
            ('Y3', 'Y3'),
            ('Y4', 'Y4'),
            ('Y5', 'Terrace Huts'),
            ('Y6', 'Estates West'),
            ('Y7', 'Y7'),
            ('Y8', 'Landscape Services Building'),
            ('Y9', 'Engineering Building'),
            ('Y10', 'Computer Science'),
            ('Y11', 'Y11'),
            ('Y12', 'Chemical Engineering'),
            ('Y13', 'Chemical Engineering Workshop'),
            ('Y14', 'Sports Pavilion'),
            ('Y15', 'Rehabilitation Sciences'),
            ('Y16', 'Sport, Exercise and Rehabilitation Laboratories'),
            ('Y17', 'Public Health'),
            ('Y18', 'Y18'),
            ('Y19', 'NBIF'),
        ]
        choices = sorted(choices, key=lambda x: x[1])
        choices.append(('Other', 'Other'))
        self.location.choices = choices


    def validate_date(self, field):
        today = datetime.utcnow().date()
        input_date = field.data.date()
        if input_date < today + timedelta(days=7):
            raise ValidationError('The activity date must be at least 7 days from today.')

class JoinLeaveActivityForm(FlaskForm):
    action = HiddenField('Action', id='action_field', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    deadline = DateTimeField('Deadline', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SubmissionForm(FlaskForm):
    content = TextAreaField('Your Answer', validators=[
        DataRequired(message="Content cannot be empty."),
        Length(min=10, max=500, message="Answer must be between 10 and 500 characters.")
    ])
    edit = HiddenField(default='')
    submit = SubmitField('Submit Assignment')
    update = SubmitField('Update Submission')

class FeedbackForm(FlaskForm):
    choice = HiddenField(validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[
        DataRequired(message="Feedback cannot be empty."),
        Length(min=5, max=300)
    ])
    submit = SubmitField('Submit Feedback')
