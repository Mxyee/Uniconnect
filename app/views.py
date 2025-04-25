from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, abort
from app import app
from app.models import User, Notification
from app.forms import ChooseForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db, mail
from urllib.parse import urlsplit
import csv
import io
import datetime
from app.notification import trigger_notification
from flask_mail import Message


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



@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', title="Notification", notifications=notifications)

@app.route('/notification/<int:id>')
@login_required
def view_notification(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.is_read = True
    db.session.commit()
    return render_template('view_notification.html',title="Notifications", notification=notification)


# test
@app.route("/test_notify")
@login_required
def test_notify():
    trigger_notification("joined_activity", user_id=current_user.id, activity_title="Flask Club")
    return "Test notify"


# test
@app.route('/test_email')
def test_email():
    try:
        msg = Message(
            subject="Test notification",
            recipients=["test@gmail.com"],
            body="This is a test message."
        )
        mail.send(msg)
        return "Test email sent!"
    except Exception as e:
        return f"<h2>Email Error:</h2><pre>{str(e)}</pre>"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/templates/errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/templates/errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/templates/errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/templates/errors/500.html', title='Error'), 500