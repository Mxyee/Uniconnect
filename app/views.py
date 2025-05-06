from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, abort
from app import app
from app.forms import ChooseForm, LoginForm, RegisterForm,FeedbackForm, CreateActivityForm,JoinLeaveActivityForm, AssignmentForm, SubmissionForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime
from app import app, db
from flask_login import current_user
from app.models import User, Activity, Assignment, Submission, Notification, Participant
from flask_mail import Message, Mail
from app.notification import trigger_notification
import sqlalchemy as sa
from datetime import datetime

@app.route("/")
def home():
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    else:
        unread_count = 0
    return render_template("home.html", title='Home', unread_count=unread_count)


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")


@app.route('/login', methods=['GET', 'POST'])#Wenjung Chen
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

@app.route('/logout')#Wenjung Chen
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/student/register', methods=['GET', 'POST'])#Wenjung Chen
def student_register():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'warning')
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        student = User(username=form.username.data, email=form.email.data, role='student')
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now registered as a student!', 'success')
        return redirect(url_for('login'))
    return render_template('student_register.html', title='Student Register', form=form)

@app.route('/professor/register', methods=['GET', 'POST'])#Wenjung Chen
def professor_register():
    if current_user.role != 'admin':
        flash('Only admins can register professor accounts', 'warning')
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        professor = User(username=form.username.data, email=form.email.data, role='professor')
        professor.set_password(form.password.data)
        db.session.add(professor)
        db.session.commit()
        flash('Congratulations, the professor account has been successfully created!', 'success')
        return redirect(url_for('login'))

    return render_template('professor_register.html', title='Professor Register', form=form)

@app.route("/activities") #Ting-Chieh Lin
def activities():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'date')
    order = request.args.get('order', 'asc')
    mine = request.args.get('mine', 'false').lower() == 'true'
    q = db.select(Activity)

    if mine:
        q = q.where(Activity.created_by == current_user.id)

    if search:
        search_like = f"%{search}%"
        q = q.filter(Activity.title.ilike(search_like))

    if sort_by == 'date':
        column = Activity.date
    elif sort_by == 'location':
        column = Activity.location
    else:
        column = Activity.title

    if order == 'desc':
        q = q.order_by(column.desc())
    else:
        q = q.order_by(column.asc())
    activities = db.session.scalars(q)
    return render_template('activities.html', activities=activities, search=search, sort_by=sort_by, order=order, title="Activities", mine=mine)

@app.route('/create_activity', methods=['GET', 'POST'])#Ting-Chieh Lin
@login_required
def create_activity():
    if current_user.role != 'student':
        flash('Only students can create activities.', 'danger')
        return redirect(url_for('home'))
    form = CreateActivityForm()
    if form.validate_on_submit():
        if form.location.data == 'Other' and not form.custom_location.data:
            flash('Please provide a custom location.', 'warning')
            return render_template('create_activity.html', title="Create Activity", form=form)

        location = form.custom_location.data if form.location.data == 'Other' else form.location.data
        activity = Activity(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=location,
            created_by=current_user.id
        )
        db.session.add(activity)
        db.session.commit()

        participant = Participant(activity_id=activity.id, student_id=current_user.id)
        db.session.add(participant)
        db.session.commit()

        trigger_notification("activity_created", user_id=current_user.id, activity_name=form.title.data)

        flash('Activity created successfully!', 'success')
        return redirect(url_for('activities'))
    return render_template('create_activity.html', title="Create Activity", form=form)

@app.route('/activity/<int:id>', methods=['GET', 'POST'])#Ting-Chieh Lin
@login_required
def activity(id):
    activity = db.session.get(Activity, id)
    if not activity:
        flash('Activity not found.', 'danger')
        return redirect(url_for('activities'))
    form = JoinLeaveActivityForm()
    if form.validate_on_submit():
        participant = db.session.scalar(
            sa.select(Participant).where(
                Participant.activity_id == activity.id,
                Participant.student_id == current_user.id
            )
        )
        is_creator = current_user.id == activity.created_by
        if form.action.data == 'join' and not participant:
            if current_user.role != 'student':
                flash('Only students can join activities.', 'danger')
                return redirect(url_for('activity', id=activity.id))
            if len(activity.participants) >= 5:
                flash('This activity is already full.', 'warning')
                trigger_notification("activity_full", user_id=activity.created_by, activity_title=activity.title)
            else:
                participant = Participant(activity_id=activity.id, student_id=current_user.id)
                db.session.add(participant)
                db.session.commit()
                trigger_notification("joined_activity", user_id=current_user.id, activity_title=activity.title)
                flash('You have joined the activity.', 'success')
                if len(activity.participants) == 5 and not activity.is_full_notified:
                    trigger_notification("activity_full", user_id=activity.created_by, activity_title=activity.title)
                    activity.is_full_notified = True
                    db.session.commit()

        elif form.action.data == 'leave':
            if not participant:
                flash('You are not a participant of this activity.', 'danger')
            else:
                now = datetime.utcnow()
                days_until_activity = (activity.date - now).days
                if days_until_activity < 3:
                    flash('You cannot leave the activity within 3 days of its start date.', 'warning')
                else:
                    db.session.delete(participant)
                    db.session.commit()
                    flash('You have left the activity.', 'success')
                    if len(activity.participants) < 5 and activity.is_full_notified:
                        activity.is_full_notified = False
                        db.session.commit()

                    if is_creator:
                        participant = db.session.scalar(
                            sa.select(Participant).where(Participant.activity_id == activity.id).limit(1)
                        )
                        if participant:
                            activity.created_by = participant.student_id
                            db.session.commit()
                            flash('New creator assigned.', 'info')
                        else:
                            # No participants left, delete the activity
                            title = activity.title
                            db.session.delete(activity)
                            db.session.commit()
                            flash(f'No participants left. "{title}" has been deleted.', 'warning')
                            return redirect(url_for('activities'))
        return redirect(url_for('activity', id=activity.id))
    is_participant = any(p.student_id == current_user.id for p in activity.participants)
    is_creator = current_user.id == activity.created_by
    now = datetime.utcnow()
    can_leave = (activity.date - now).days >= 3
    return render_template('activity.html', title='activity_details', activity=activity, form=form, is_participant=is_participant, is_creator=is_creator, now=now,
    can_leave=can_leave)


@app.route('/activity/<int:id>/edit', methods=['GET', 'POST'])#Ting-Chieh Lin
@login_required
def edit_activity(id):
    activity = db.session.get(Activity, id)
    if not activity:
        flash('Activity not found.', 'danger')
        return redirect(url_for('activities'))
    if current_user.id != activity.created_by:
        flash('You are not authorized to edit this activity.', 'danger')
        return redirect(url_for('activities'))
    if activity.date < datetime.utcnow():
        flash('You cannot edit a past activity.', 'warning')
        return redirect(url_for('activity', id=activity.id))
    form = CreateActivityForm(obj=activity)
    if form.validate_on_submit():
        if form.location.data == 'Other' and not form.custom_location.data:
            flash('Please provide a custom location.', 'warning')
            return render_template('create_activity.html', title="Edit Activity", form=form)

        activity.title = form.title.data
        activity.description = form.description.data
        activity.date = form.date.data
        activity.location = form.custom_location.data if form.location.data == 'Other' else form.location.data

        db.session.commit()
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('activity', id=activity.id))
    if activity.location not in dict(form.location.choices):
        form.location.data = 'Other'
        form.custom_location.data = activity.location
    else:
        form.location.data = activity.location
    return render_template('create_activity.html', title="Edit Activity", form=form)

@app.route('/assignments')#Haoyang Zhao
@login_required
def assignments():
    if current_user.role == 'professor':
        # if the current user is a professor, show their own assignments
        q = db.select(Assignment).where(Assignment.professor_id == current_user.id)
    else:
        # for students, show all assignments
        q = db.select(Assignment)

    # users can search for assignments
    search = request.args.get('search')
    if search:
        q = q.where(Assignment.title.ilike(f"%{search}%"))
    assignments = db.session.scalars(q)
    return render_template('assignments.html', title="Assignments", assignments=assignments)

@app.route('/new_assignment', methods=['GET', 'POST'])#Haoyang Zhao
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

@app.route('/assignment/<int:assignment_id>', methods=['GET', 'POST'])#Haoyang Zhao&Ming-Ye Chan
@login_required
def assignment_detail(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        flash("Assignment not found", "danger")
        return redirect(url_for('assignments'))

    submission = db.session.scalar(
        db.select(Submission).where(
            (Submission.assignment_id == assignment.id) &
            (Submission.student_id == current_user.id)
        )
    ) if current_user.role == 'student' else None

    submission_form = SubmissionForm()
    feedback_form = FeedbackForm()
    choose_form = ChooseForm()

    # 🎯 STUDENT submits or edits submission
    if current_user.role == 'student' and submission_form.validate_on_submit():
        if not submission:
            submission = Submission(
                assignment_id=assignment.id,
                student_id=current_user.id,
                content=submission_form.content.data,
                status="submitted"
            )
            db.session.add(submission)
        else:
            submission.content = submission_form.content.data
            submission.status = "modified"
        db.session.commit()
        flash("Submission saved", "success")
        return redirect(url_for('assignment_detail', assignment_id=assignment.id))

    # 🎯 PROFESSOR submits feedback
    if current_user.role == 'professor' and feedback_form.validate_on_submit():
        sub_id = int(feedback_form.choice.data)
        sub = db.session.get(Submission, sub_id)
        if sub:
            sub.feedback = feedback_form.feedback.data
            db.session.commit()
            flash("Feedback submitted", "success")
            return redirect(url_for('assignment_detail', assignment_id=assignment.id))

    return render_template('assignment_detail.html',
                           title='Assignment Detail',
                           assignment=assignment,
                           submission=submission,
                           submission_form=submission_form,
                           feedback_form=feedback_form,
                           choose_form=choose_form)


@app.route("/edit_assignment/<int:assignment_id>", methods=['GET', 'POST'])#Haoyang Zhao
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
        return redirect(url_for('assignment_detail', assignment_id=assignment.id))
    return render_template('generic_form.html', title='Edit Assignment', form=form)

@app.route('/assignment/<int:assignment_id>/delete', methods=['POST'])#Haoyang Zhao
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

@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])#Ming-Ye Chan
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
            trigger_notification("assignment_submitted", user_id=current_user.id, assignment_title=assignment.title)
            flash("Your submission has been saved.", "success")
            return redirect(url_for('my_assignments'))
        except Exception as e:
            db.session.rollback()
            flash("Database error occurred.", "danger")
            print("DB ERROR:", e)

    if submission:
        form.content.data = submission.content

    return render_template('assignment_detail.html', title=f'Submit: {assignment.title}', assignment=assignment, form=form, submission=submission)

@app.route('/give_feedback', methods=['POST'])#Ming-Ye Chan
@login_required
def give_feedback():
    if current_user.role != 'professor':
        flash("Only professors can give feedback.", "danger")
        return redirect(url_for('home'))

    form = FeedbackForm()

    if form.validate_on_submit():
        try:
            submission_id = int(form.choice.data)
            submission = db.session.get(Submission, submission_id)

            if submission is None:
                flash("Submission not found.", "danger")
                return redirect(request.referrer or url_for('assignments'))

            submission.feedback = form.feedback.data
            db.session.commit()

            from app.notification import trigger_notification
            trigger_notification(
                'feedback_given',
                user_id=submission.student_id,
                assignment_title=submission.assignment.title
            )

            flash("Feedback submitted.", "success")
            return redirect(url_for('assignments'))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting feedback.", "danger")
            print("Feedback error:", e)
    else:
        flash("Invalid feedback form data.", "danger")

    # Redirect back to the assignment detail page
    assignment_id = submission.assignment_id if 'submission' in locals() else None
    return redirect(url_for('assignment_detail', assignment_id=assignment_id))



@app.route('/delete_submission/<int:submission_id>', methods=['POST'])#Ming-Ye Chan
@login_required
def delete_submission(submission_id):
    submission = db.session.get(Submission, submission_id)
    if not submission or submission.student_id != current_user.id:
        flash("You are not allowed to delete this submission.", "danger")
        return redirect(url_for('assignments'))

    db.session.delete(submission)
    db.session.commit()
    flash('Submission deleted.', 'info')
    return redirect(url_for('assignments'))

@app.route("/edit_submission/<int:submission_id>", methods=['GET', 'POST'])#Ming-Ye Chan
@login_required
def edit_submission(submission_id):
    submission = db.session.get(Submission, submission_id)
    if not submission:
        flash('Submission not found.', 'danger')
        return redirect(url_for('assignments'))

    # make sure be edited by students
    if submission.student_id != current_user.id:
        flash('You do not have permission to edit this submission.', 'danger')
        return redirect(url_for('assignments'))

    form = SubmissionForm(obj=submission)
    form.edit.data = "true"
    form.submit.render_kw = {"style": "display:none"}
    if form.validate_on_submit():
        submission.content = form.content.data
        submission.status = "modified"
        db.session.commit()
        flash('Submission updated successfully!', 'success')
        return redirect(url_for('assignment_detail', assignment_id=submission.assignment_id))

    return render_template('generic_form.html', title='Edit Submission', form=form)


@app.route('/notifications')#Ying-Hsin Hua
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', title="Notification", notifications=notifications)


@app.route('/notification/<int:id>')#Ying-Hsin Hua
@login_required
def view_notification(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.is_read = True
    db.session.commit()
    return render_template('view_notification.html',title="Notifications", notification=notification)



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

