from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Assignment, Submission
from app.forms import ChooseForm, LoginForm, SubmissionForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime


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

@app.route('/my_assignments')
@login_required
def my_assignments():
    if current_user.role != 'student':
        return redirect(url_for('home'))

    # Only show assignments that the student hasn't submitted yet
    submitted_ids = db.session.scalars(
        sa.select(Submission.assignment_id).where(Submission.student_id == current_user.id)
    ).all()

    assignments = db.session.scalars(
        sa.select(Assignment).where(~Assignment.id.in_(submitted_ids))
    ).all()

    return render_template("my_assignments.html", title='My Assignments', assignments=assignments)
@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    if current_user.role != 'student':
        return redirect(url_for('home'))

    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        flash("Assignment not found.", "danger")
        return redirect(url_for('my_assignments'))

    # Check if this student already submitted
    submission = db.session.scalar(
        sa.select(Submission).where(
            (Submission.assignment_id == assignment.id) &
            (Submission.student_id == current_user.id)
        )
    )

    form = SubmissionForm()

    if form.validate_on_submit():
        try:
            if submission is None:
                new_submission = Submission(
                    assignment_id=assignment.id,
                    student_id=current_user.id,
                    content=form.content.data,
                    status="submitted"
                )
                db.session.add(new_submission)
            else:
                submission.status = "modified"
                submission.content = form.content.data

            db.session.commit()
            flash("Your submission has been saved.", "success")
            return redirect(url_for('my_assignments'))
        except Exception as e:
            db.session.rollback()
            flash("Database error occurred.", "danger")
            print("DB ERROR:", e)

    if submission:
        form.content.data = submission.content

    return render_template('submission_form.html', title=f'Submit: {assignment.title}', assignment=assignment, form=form, submission=submission)

@app.route('/give_feedback/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(submission_id):
    if current_user.role != 'professor':
        return redirect(url_for('home'))
    submission = db.session.get(Submission, submission_id)
    if submission is None:
        flash("Submission not found, student did not submit the assignment", 'danger')
        return redirect(url_for('give_feedback'))


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