from app import db
from app.models import User, Assignment, Submission
import datetime

def reset_db():
    db.drop_all()
    db.create_all()

    # Create admin user
    admin = User(username='admin', email='admin@sys.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)

    # Create professors and students
    users = [
        {'username': 'prof1', 'email': 'prof1@b.com', 'role': 'professor', 'pw': '123'},
        {'username': 'prof2', 'email': 'prof2@b.com', 'role': 'professor', 'pw': '123'},
        {'username': 'mingye', 'email': 'mingye@stu.com', 'role': 'student', 'pw': '123'},
        {'username': 'jo', 'email': 'jo@stu.com', 'role': 'student', 'pw': '123'},
        {'username': 'tariq', 'email': 'tariq@stu.com', 'role': 'student', 'pw': '123'},
    ]

    user_objs = []
    for u in users:
        pw = u.pop('pw')
        user = User(**u)
        user.set_password(pw)
        db.session.add(user)
        user_objs.append(user)
    db.session.commit()

    # Create test assignment by prof1
    assignment = Assignment(
        title="Assignment 1",
        description="This is a test assignment.",
        deadline=datetime.datetime(2025, 5, 5),
        professor_id=user_objs[0].id
    )
    db.session.add(assignment)
    db.session.commit()

    # Create submission by mingye
    submission = Submission(
        assignment_id=assignment.id,
        student_id=user_objs[2].id,
        content="Here is my answer for Assignment 1.",
        status="submitted",
        feedback="Good job!"
    )
    db.session.add(submission)
    db.session.commit()

    print("✅ Database has been reset with test users including admin.")
