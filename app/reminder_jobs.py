from datetime import datetime, timedelta, timezone
from app import db
from app.models import Activity
from app.notification import trigger_notification

def send_activity_reminders():
    now = datetime.now(timezone.utc)
    target_date = now + timedelta(days=3)

    activities = db.session.query(Activity).filter(Activity.date != None).all()

    for act in activities:
        if act.date.date() == target_date.date():
            trigger_notification("activity_reminder", user_id=act.created_by, activity_title=act.title, activity_date=act.date.strftime('%Y-%m-%d %H:%M'))
            for p in act.participants:
                trigger_notification("activity_reminder", user_id=p.student_id, activity_title=act.title, activity_date=act.date.strftime('%Y-%m-%d %H:%M'))