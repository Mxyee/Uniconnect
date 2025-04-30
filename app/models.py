from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
from datetime import datetime

# User Table（Student,Professor、Admin）
@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="student")  # student, professor, admin

    submissions: so.Mapped[List['Submission']] = relationship(back_populates='student', cascade='all, delete-orphan')
    assignments: so.Mapped[List['Assignment']] = relationship(back_populates='professor', cascade='all, delete-orphan')
    activities_created: so.Mapped[List['Activity']] = relationship(back_populates='creator', cascade='all, delete-orphan')
    notifications: so.Mapped[List['Notification']] = relationship(back_populates='user', cascade='all, delete-orphan')
    participations: so.Mapped[List['Participant']] = relationship(back_populates='student', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, role={self.role})'

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='professor', uselist=False)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Assignment Table
@dataclass
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    deadline: so.Mapped[str] = so.mapped_column(sa.String(64))
    professor_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))
    professor: so.Mapped['User'] = relationship(back_populates='assignments')

    submissions: so.Mapped[List['Submission']] = relationship(back_populates='assignment', cascade='all, delete-orphan')

# Assignment Submission Table
@dataclass
class Submission(db.Model):
    __tablename__ = 'submissions'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    assignment_id: so.Mapped[int] = so.mapped_column(ForeignKey('assignments.id'))
    student_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))
    status: so.Mapped[str] = so.mapped_column(sa.String(20))
    content: so.Mapped[str] = so.mapped_column(sa.Text)
    feedback: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)


    assignment: so.Mapped['Assignment'] = relationship(back_populates='submissions')
    student: so.Mapped['User'] = relationship(back_populates='submissions')

    def __init__(self, assignment_id, student_id, status, content, feedback=None):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.status = status
        self.content = content
        self.feedback = feedback

# Student Activities Table
@dataclass
class Activity(db.Model):
    __tablename__ = 'activities'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    location: so.Mapped[str] = so.mapped_column(sa.String(128))
    created_by: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))

    creator: so.Mapped['User'] = relationship(back_populates='activities_created')
    participants: so.Mapped[List['Participant']] = relationship(back_populates='activity', cascade='all, delete-orphan')

# Activity Participant Table （Many to many）
@dataclass
class Participant(db.Model):
    __tablename__ = 'participants'

    activity_id: so.Mapped[int] = so.mapped_column(ForeignKey('activities.id'), primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'), primary_key=True)

    activity: so.Mapped['Activity'] = relationship(back_populates='participants')
    student: so.Mapped['User'] = relationship(back_populates='participations')

# Notifications Table
@dataclass
class Notification(db.Model):
    __tablename__ = 'notifications'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))
    message: so.Mapped[str] = so.mapped_column(sa.Text)
    date: so.Mapped[str] = so.mapped_column(sa.String(64))

    user: so.Mapped['User'] = relationship(back_populates='notifications')

