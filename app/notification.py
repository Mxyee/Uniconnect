from app import db, mail
from app.models import User, Notification
from flask_mail import Message
from flask import render_template



def notify(user_id, message, send_email=True):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()
    if send_email:
        try:
            user = User.query.get(user_id)
            if user and user.email:
                try:
                    html = render_template('email_notification.html', user=user, message=message)
                except Exception as e:
                    print(f"[Template Error] Failed to render email for user_id={user_id}: {e}")
                    html = None
                msg = Message(subject="New Notification", recipients=[user.email], body=message)
                if html:
                    msg.html = html
                mail.send(msg)
                print(f"Email sent to {user.email}")
            else:
                print(f"[Notify] User {user_id} not found or has no email.")
        except Exception as e:
            print(f"[Mail Error] Failed to send email to user_id={user_id}:", e)


def trigger_notification(event_type, **kwargs):
    if event_type == "joined_activity":
        notify(kwargs['user_id'], f"You have successfully joined the activity: {kwargs['activity_title']}")

    elif event_type == "assignment_submitted":
        notify(kwargs['user_id'], f"You have submitted your assignment: {kwargs['assignment_title']}")

    elif event_type == "activity_created":
        notify(kwargs['user_id'], f"You have created a new activity: {kwargs['activity_name']}")

    elif event_type == "feedback_given":
        notify(kwargs['user_id'], f"You received feedback from your instructor on: {kwargs['assignment_title']}")

    elif event_type == "activity_full":
        notify(kwargs['user_id'], f"The activity '{kwargs['activity_title']}' has reached full capacity.")

    elif event_type == "activity_reminder":
        notify(kwargs['user_id'], f"Reminder: The activity '{kwargs['activity_title']}' will start at {kwargs['activity_date']}.")