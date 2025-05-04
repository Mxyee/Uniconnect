from app import db
from app.models import User, Assignment, Submission, Activity, Participant, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime

def reset_db():
    db.drop_all()
    db.create_all()

    # Create users
    prof1 = User(username='prof_lee', email='lee@uni.edu', role='professor')
    prof1.set_password('lee123')
    prof2 = User(username='prof_kim', email='kim@uni.edu', role='professor')
    prof2.set_password('kim123')

    stu1 = User(username='alice', email='alice@student.edu', role='student')
    stu1.set_password('alice123')
    stu2 = User(username='bob', email='bob@student.edu', role='student')
    stu2.set_password('bob123')
    stu3 = User(username='carol', email='carol@student.edu', role='student')
    stu3.set_password('carol123')
    stu4 = User(username='david', email='david@student.edu')
    stu4.set_password('david123')
    stu5 = User(username='eve', email='eve@student.edu')
    stu5.set_password('eve123')
    stu6 = User(username='frank', email='frank@student.edu')
    stu6.set_password('frank123')

    db.session.add_all([prof1, prof2, stu1, stu2, stu3, stu4, stu5, stu6])
    db.session.commit()

    #Creat an admin
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
        role='admin'
    )

    db.session.add(admin)
    db.session.commit()

    # Create assignments
    a1 = Assignment(title='Math Homework 1', description='Calculus problems',
                    deadline=datetime.strptime('2025-05-10', '%Y-%m-%d'), professor_id=prof1.id)
    a2 = Assignment(title='Physics Lab', description='Submit lab report',
                    deadline=datetime.strptime('2025-05-10', '%Y-%m-%d'), professor_id=prof2.id)
    a3 = Assignment(title='Programming Project', description='Build a Flask app',
                    deadline=datetime.strptime('2025-05-10', '%Y-%m-%d'), professor_id=prof1.id)
    db.session.add_all([a1, a2, a3])
    db.session.commit()

    # Submissions
    s1 = Submission(assignment_id=a1.id, student_id=stu1.id, status='submitted', content='Completed all integrals.',feedback='Good job!')
    s2 = Submission(assignment_id=a2.id, student_id=stu2.id, status='submitted', content='Lab report in PDF.',feedback='Please fix formatting.')
    s3 = Submission(assignment_id=a3.id, student_id=stu3.id, status='submitted', content='Flask app built with login.',feedback='Excellent!')

    db.session.add_all([s1, s2, s3])
    db.session.commit()

    # Activities
    act1 = Activity(title='AI Study Group', description='Discuss ML topics', date=datetime(2025, 5, 1, 15, 30), location='Room 101', created_by=stu1.id)
    act2 = Activity(title='Startup Club Meetup', description='Pitch ideas and get feedback', date=datetime(2025, 5, 7, 10, 0), location='Library Hall', created_by=stu2.id)

    db.session.add_all([act1, act2])
    db.session.commit()

    # Participants
    db.session.add_all([
        Participant(activity_id=act1.id, student_id=stu1.id),
        Participant(activity_id=act1.id, student_id=stu3.id),
        Participant(activity_id=act2.id, student_id=stu2.id)
    ])
    db.session.commit()

    # Notifications
    n1 = Notification(user_id=stu1.id, message='Assignment Math Homework 1 is due soon!',
                      timestamp=datetime(2025, 4, 20, 16, 20))
    n2 = Notification(user_id=stu3.id, message='You have joined AI Study Group.',
                      timestamp=datetime(2025, 4, 22, 19, 0))
    n3 = Notification(user_id=prof1.id, message='New submission received for Programming Project.',
                      timestamp=datetime(2025, 4, 23, 23, 8))
    db.session.add_all([n1, n2, n3])
    db.session.commit()


print("Test database initialized with sample")