from app import db, mail
from app.models import User, Notification
import sqlalchemy as sa
from flask_mail import Message


def notify(user_id, message, send_email=True):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()

    if send_email:
        try:
            user = User.query.get(user_id)
            if user and user.email:
                msg = Message(subject="You have a new notification",
                              recipients=[user.email],
                              body=message)
                mail.send(msg)
        except Exception as e:
            print(f"[Mail Error] Failed to send email to user_id={user_id}:", e)


def trigger_notification(event_type, **kwargs):
    if event_type == "joined_activity":
        notify(kwargs['user_id'], f"You have successfully joined the activity: {kwargs['activity_title']}")

    elif event_type == "assignment_submitted":
        notify(kwargs['professor_id'], f"{kwargs['student_name']} has submitted an assignment")

    elif event_type == "activity_created":
        notify(kwargs['user_id'], f"You have created a new activity: {kwargs['activity_name']}")

    elif event_type == "feedback_given":
        notify(kwargs['user_id'], f"You received feedback from your instructor on: {kwargs['assignment_title']}")

    elif event_type == "grade_published":
        notify(kwargs['user_id'], f"Your grade for {kwargs['assignment_title']} is now available")