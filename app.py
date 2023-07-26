import os
from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from admin import StudentAdmin, LecturerAdmin, ChatAdmin, FAQAdmin, OpinionAdmin
from models import Student, Lecturer, Chat, FAQ, Opinion
from forms import StudentRegistrationForm, LecturerRegistrationForm, StudentLoginForm, LecturerLoginForm, AdminLoginForm
from database import db
from flask_socketio import SocketIO, emit, join_room
from flask_admin import Admin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
STATIC_DIR = 'static/'
UPLOAD_FOLDER = 'static/images/'



db.init_app(app)
migrate = Migrate(app, db)
app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

admin = Admin(app, name='Dashboard', template_mode='bootstrap4')
admin.add_view(StudentAdmin(Student, db.session))
admin.add_view(LecturerAdmin(Lecturer, db.session))
admin.add_view(ChatAdmin(Chat, db.session))
admin.add_view(FAQAdmin(FAQ, db.session))
admin.add_view(OpinionAdmin(Opinion, db.session))


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', logged_in=True)
    else:
        return render_template('home.html', logged_in=False)


@app.route('/student', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(matric_no=form.matric_no.data).first()
        if student and student.check_password(form.password.data):
            session['student_id'] = student.id
            session['student_matric_no'] = student.matric_no
            session['student_name'] = student.lastname
            return redirect(url_for('student_dashboard'))
        else:
            flash({'message': 'Invalid username or password', 'type': 'danger'})
    return render_template('student_login.html', form=form)


@app.route('/lecturer', methods=['GET', 'POST'])
def lecturer_login():
    form = LecturerLoginForm()
    if form.validate_on_submit():
        lecturer = Lecturer.query.filter_by(staff_id=form.staff_id.data).first()
        if lecturer and lecturer.check_password(form.password.data):
            session['lecturer_id'] = lecturer.id
            session['lecturer_staff_id'] = lecturer.staff_id
            session['lecturer_name'] = lecturer.lastname
            return redirect(url_for('lecturer_dashboard'))
        else:
            flash({'message': 'Invalid username or password', 'type': 'danger'})
    return render_template('lecturer_login.html', form=form)



@app.route('/logout')
def logout():
    session.pop('username', None)
    flash({'message': 'Logged out successfully', 'type': 'success'})
    return redirect(url_for('home'))


@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['admin_email'] = admin.email
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('admin_login.html', form=form)




@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        # Check if the matriculation number and email are already registered
        existing_student = Student.query.filter_by(matric_no=form.matric_no.data).first()
        existing_email = Student.query.filter_by(email=form.email.data).first()
        if existing_student:
            flash({'message': 'Matriculation number already registered. Please log in.', 'type': 'warning'})
            return redirect(url_for('student_login'))
        elif existing_email:
            flash({'message': 'Email already registered. Please log in.', 'type': 'warning'})
            return redirect(url_for('student_login'))
        else:
            if form.password.data != form.confirm_password.data:
                flash({'message': 'Password and Confirm Password do not match.', 'type': 'danger'})
                return render_template('student_register.html', form=form)
            else:
                profile_image = form.profile_image.data
                if profile_image:
                    # Save the profile image
                    filename = secure_filename(form.matric_no.data + '.' + profile_image.filename.rsplit('.', 1)[1])
                    profile_image.save(os.path.join(app.root_path, UPLOAD_FOLDER,'students', filename))
                else:
                    filename = 'default-profile-image.jpg'  # Provide a default image if no profile image is uploaded

                student = Student(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    matric_no=form.matric_no.data,
                    email=form.email.data,
                    level=form.level.data,
                    password=generate_password_hash(form.password.data),
                    profile_image=filename  # Save the filename to the student's profile
                )
                db.session.add(student)
                db.session.commit()
                flash({'message': 'Registration successful. Please log in.', 'type': 'success'})
                return redirect(url_for('student_login'))
    return render_template('student_register.html', form=form)


@app.route('/lecturer/register', methods=['GET', 'POST'])
def lecturer_register():
    form = LecturerRegistrationForm()
    if form.validate_on_submit():
        existing_lecturer = Lecturer.query.filter_by(staff_id=form.staff_id.data).first()
        existing_email = Lecturer.query.filter_by(email=form.email.data).first()
        if existing_lecturer:
            flash({'message': 'Staff ID already registered. Please log in.', 'type': 'warning'})
            return redirect(url_for('lecturer_login'))
        elif existing_email:
            flash({'message': 'Email already registered. Please log in.', 'type': 'warning'})
            return redirect(url_for('lecturer_login'))
        else:
            if form.password.data != form.confirm_password.data:
                flash({'message': 'Password and Confirm Password do not match.', 'type': 'danger'})
                return render_template('lecturer_register.html', form=form)
            else:
                profile_image = form.profile_image.data
                if profile_image:
                    # Save the profile image
                    filename = secure_filename(form.staff_id.data + '.' + profile_image.filename.rsplit('.', 1)[1])
                    profile_image.save(os.path.join(app.root_path, UPLOAD_FOLDER,'lecturers', filename))
                else:
                    filename = 'default-profile-image.jpg'  # Provide a default image if no profile image is uploaded

                lecturer = Lecturer(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    staff_id=form.staff_id.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    profile_image=filename
                )
                db.session.add(lecturer)
                db.session.commit()
                flash({'message': 'Registration successful. Please log in.', 'type': 'success'})
                return redirect(url_for('lecturer_login'))
    return render_template('lecturer_register.html', form=form)





# Define the routes for the student and lecturer dashboards
@app.route('/student/dashboard')
def student_dashboard():
    # Retrieve the student's conversations and pass them to the template
    student_id = session['student_id']
    student = Student.query.get(session.get('student_id'))
    lecturers = Lecturer.query.all()
    faqs = FAQ.query.all()
    opinions = Opinion.query.all()
    return render_template('student_dashboard.html', lecturers=lecturers, student=student, faqs=faqs, opinions=opinions)

@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    # Retrieve the lecturer's conversations and pass them to the template
    lecturer_id = session['lecturer_id']
    lecturer = Lecturer.query.get(session.get('lecturer_id'))
    students = Student.query.all()
    return render_template('lecturer_dashboard.html', students=students, lecturer=lecturer)

def save_message_to_database(sender, receiver, message):
    new_message = Chat(sender=sender, receiver=receiver, message=message)
    db.session.add(new_message)
    db.session.commit()
    return new_message.id


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('student_message')
def handle_student_message(data):
    message = data['message']
    sender = data['sender']
    receiver = data['receiver']

    # Save the message to the database without a tracking ID
    save_message_to_database(sender, receiver, message)

    # Emit the message to the corresponding lecturer
    socketio.emit('lecturer_message', {'message': message, 'sender': sender, 'receiver': receiver}, room=receiver)
    socketio.emit('lecturer_message', {'message': message, 'sender': sender, 'receiver': receiver}, room=sender)

@socketio.on('lecturer_message')
def handle_lecturer_message(data):
    message = data['message']
    sender = data['sender']
    receiver = data['receiver']

    # Save the message to the database without a tracking ID
    save_message_to_database(sender, receiver, message)
    print(receiver)
    # Emit the message to the corresponding student
    socketio.emit('student_message', {'message': message, 'sender': sender, 'receiver': receiver}, room=receiver)


@app.route('/lecturer/chat/history', methods=['POST'])
def retrieve_lecturer_chat_history():
    student_matric_no = request.form.get('student_matric_no')
    lecturer_id = session.get('lecturer_staff_id')

    # Retrieve the chat history between lecturer and student from the database
    chat_history = Chat.query.filter(
        ((Chat.sender == lecturer_id) & (Chat.receiver == student_matric_no)) |
        ((Chat.sender == student_matric_no) & (Chat.receiver == lecturer_id))
    ).all()

    # Convert the chat history to a list of dictionaries
    chat_history_list = []
    for message in chat_history:
        chat_history_list.append({
            'sender': message.sender,
            'message': message.message
        })

    # Return the chat history as JSON response
    return jsonify(chat_history_list)

@app.route('/student/chat/history', methods=['POST'])
def retrieve_student_chat_history():
    student_matric_no = session.get('student_matric_no')
    lecturer_id = request.form.get('lecturer_id')

    # Retrieve the chat history between lecturer and student from the database
    chat_history = Chat.query.filter(
        ((Chat.sender == lecturer_id) & (Chat.receiver == student_matric_no)) |
        ((Chat.sender == student_matric_no) & (Chat.receiver == lecturer_id))
    ).all()

    # Convert the chat history to a list of dictionaries
    chat_history_list = []
    for message in chat_history:
        chat_history_list.append({
            'sender': message.sender,
            'message': message.message
        })

    # Return the chat history as JSON response
    return jsonify(chat_history_list)

@app.route('/student/get_data', methods=['POST'])
def get_student_data():
    matric_no = request.form.get('matric_no')

    # Retrieve the student data from the database based on the matriculation number
    student = Student.query.filter_by(matric_no=matric_no).first()

    if student:
        # Prepare the student data to be sent as JSON
        student_data = {
            'firstname': student.firstname,
            'lastname': student.lastname,
            'profile_image': student.profile_image,
            'level': student.level
        }
        return jsonify(student_data)
    else:
        return jsonify({'error': 'Student not found'})




if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host = '192.168.246.186')
