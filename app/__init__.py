from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_mail import Mail


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)


from app import views, models
from app.debug_utils import reset_db

from flask_login import current_user
from app.models import Notification

@app.context_processor
def inject_unread_count():
    if current_user.is_authenticated:
        count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    else:
        count = 0
    return dict(unread_count=count)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)

from app import scheduled_reminders