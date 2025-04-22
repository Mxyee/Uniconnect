from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Professor  # 假设你有一个Professor模型
from app.forms import ChooseForm, LoginForm, ProfessorLoginForm, ProfessorRegisterForm, StudentRegisterForm  # 假设你有这些表单
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime
from app import app, db
from flask_login import current_user
from app.models import User
import sqlalchemy as sa


@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/professor/register', methods=['GET', 'POST'])
def professor_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ProfessorRegisterForm()
    if form.validate_on_submit():
        professor = Professor(username=form.username.data)
        professor.set_password(form.password.data)
        db.session.add(professor)
        db.session.commit()
        flash('Congratulations, you are now a registered professor!', 'success')
        return redirect(url_for('professor_login'))
    return render_template('generic_form.html', title='Professor Register', form=form)


@app.route('/professor/login', methods=['GET', 'POST'])
def professor_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ProfessorLoginForm()
    if form.validate_on_submit():
        professor = db.session.scalar(
            sa.select(Professor).where(Professor.username == form.username.data))
        if professor is None or not professor.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('professor_login'))
        login_user(professor, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Professor Sign In', form=form)


@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'warning')
        return redirect(url_for('home'))

    form = StudentRegisterForm()
    if form.validate_on_submit():
        student = User(username=form.username.data, email=form.email.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now registered as a student!', 'success')
        return redirect(url_for('login'))

    return render_template('student_register.html', title='Student Register', form=form)

# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500


