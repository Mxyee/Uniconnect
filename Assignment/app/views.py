from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Assignment
from app.forms import ChooseForm, LoginForm, AssignmentForm
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/assignments')
def assignments():
    if current_user.role == 'professor':
        # if the current user is a professor, show their own assignments
        q = db.select(Assignment).where(Assignment.professor_id == current_user.id)
    else:
        # for students, show all assignments
        q = db.select(Assignment)
    assignments = db.session.scalars(q)
    return render_template('assignments.html', title="Assignments", assignments=assignments)

@app.route('/new_assignment', methods=['GET', 'POST'])
@login_required
def new_assignment():
    # only professor can create new assignment
    if current_user.role != 'professor':
        flash('You do not have permission to create an assignment.', 'danger')
        return redirect(url_for('home'))

    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data,
            professor_id=current_user.id
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('assignments'))
    return render_template('generic_form.html', title='New Assignment', form=form)

@app.route("/assignment/<int:assignment_id>", methods=['GET', 'POST'])
@login_required
def assignment(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        flash('Assignment not found.', 'danger')
        return redirect(url_for('assignments'))
    return render_template('assignment_detail.html', title="Assignment", assignment=assignment)

@app.route("/edit_assignment/<int:assignment_id>", methods=['GET', 'POST'])
@login_required
def edit_assignment(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        flash('Assignment not found.', 'danger')
        return redirect(url_for('assignments'))

    # only the owner professor can edit this assignment
    if assignment.professor_id != current_user.id:
        flash('You do not have permission to edit this assignment.', 'danger')
        return redirect(url_for('assignments'))
    form = AssignmentForm(obj=assignment)
    if form.validate_on_submit():
        assignment.title = form.title.data
        assignment.description = form.description.data
        assignment.deadline = form.deadline.data
        db.session.commit()
        flash('Assignment updated successfully!', 'success')
        return redirect(url_for('assignment', assignment_id=assignment.id))
    return render_template('generic_form.html', title='Edit Assignment', form=form)

@app.route('/assignment/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        flash('Assignment not found.', 'danger')
        return redirect(url_for('assignments'))

    # only the owner professor can delete
    if current_user.role != 'professor' or assignment.professor_id != current_user.id:
        flash('You do not have permission to delete this assignment.', 'danger')
        return redirect(url_for('assignments'))

    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted successfully!', 'success')
    return redirect(url_for('assignments'))

# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500