from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import sqlalchemy as sa
import sqlalchemy.orm as so
# from app.models import Notification
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

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)


# @app.context_processor
# def inject_unread_count():
#     if current_user.is_authenticated:
#         unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
#         return dict(unread_count=unread)
#     return dict(unread_count=0)