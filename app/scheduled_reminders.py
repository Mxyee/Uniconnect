from apscheduler.schedulers.background import BackgroundScheduler
from app.reminder_jobs import send_activity_reminders
from datetime import timezone
from app import app

def job():
    with app.app_context():
        send_activity_reminders()

scheduler = BackgroundScheduler(timezone=timezone.utc)
scheduler.add_job(job, 'interval', days=1)
scheduler.start()
print("Daily activity reminder scheduler is running.")
