from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    deadline: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime)
    professor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    professor= db.relationship("User", backref="assignments")

class Submission(db.Model):
    __tablename__ = 'submissions'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    assignment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('assignments.id'))
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    content: so.Mapped[str] = so.mapped_column(sa.Text)
    status: so.Mapped[str] = so.mapped_column(sa.String(20), default="submitted")
    feedback: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    assignment = db.relationship("Assignment", backref="submissions")
    student = db.relationship("User", backref="submissions")

