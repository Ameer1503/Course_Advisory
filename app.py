from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

from admin import StudentAdmin, LecturerAdmin, ChatAdmin, FAQAdmin
from models import Student, Lecturer, Chat, FAQ
from forms import StudentRegistrationForm, LecturerRegistrationForm, StudentLoginForm, LecturerLoginForm, AdminLoginForm
from database import db
from flask_socketio import SocketIO, emit, join_room
from flask_admin import Admin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'



db.init_app(app)
migrate = Migrate(app, db)
app.debug = True

socketio = SocketIO(app, cors_allowed_origins="*")

admin = Admin(app, name='Dashboard', template_mode='bootstrap4')
admin.add_view(StudentAdmin(Student, db.session))
admin.add_view(LecturerAdmin(Lecturer, db.session))
admin.add_view(ChatAdmin(Chat, db.session))
admin.add_view(FAQAdmin(FAQ, db.session))

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', logged_in=True)
    else:
        return render_template('home.html', logged_in=False)

# @app.route('/login')
# def admin_login():
#         return render_template('admin_login.html'form=form)

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
            flash('Invalid username or password', 'danger')
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
            flash('Invalid username or password', 'danger')
    return render_template('lecturer_login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
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
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('admin_login.html', form=form)


@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        existing_student = Student.query.filter_by(matric_no=form.matric_no.data).first()
        if existing_student:
            flash('Matriculation number already registered. Please log in.', 'warning')
            return redirect(url_for('student_login'))
        else:
            student = Student(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                matric_no=form.matric_no.data,
                email= form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(student)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('student_login'))
    return render_template('student_register.html', form=form)


@app.route('/lecturer/register', methods=['GET', 'POST'])
def lecturer_register():
    form = LecturerRegistrationForm()
    if form.validate_on_submit():
        existing_lecturer = Lecturer.query.filter_by(staff_id=form.staff_id.data).first()
        if existing_lecturer:
            flash('Staff ID already registered. Please log in.', 'warning')
            return redirect(url_for('lecturer_login'))
        else:
            lecturer = Lecturer(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                staff_id=form.staff_id.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(lecturer)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('lecturer_login'))
    return render_template('lecturer_register.html', form=form)


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        # TODO: Implement admin dashboard
        return render_template('admin_dashboard.html', current_user=current_user)
    else:
        return redirect(url_for('admin_login'))




# Define the routes for the student and lecturer dashboards
@app.route('/student/dashboard')
def student_dashboard():
    # Retrieve the student's conversations and pass them to the template
    student_id = session['student_id']
    student = Student.query.first()
    lecturers = Lecturer.query.all()
    faqs = FAQ.query.all()
    return render_template('student_dashboard.html', lecturers=lecturers, student=student, faqs=faqs)

@app.route('/lecturer/dashboard')
def lecturer_dashboard():
    # Retrieve the lecturer's conversations and pass them to the template
    lecturer_id = session['lecturer_id']
    lecturer = Lecturer.query.first()
    students = Student.query.all()
    return render_template('lecturer_dashboard.html', students=students, lecturer=lecturer)

# Add the chat-related SocketIO events
# @socketio.on('message')
# def handle_message(data):
#     student_id = data['student_id']
#     lecturer_id = data['lecturer_id']
#     message = data['message']
#
#     # Save the message to the database
#     conversation = Conversation.query.filter_by(student_id=student_id, lecturer_id=lecturer_id).first()
#     if not conversation:
#         # If the conversation doesn't exist, create a new one
#         conversation = Conversation(student_id=student_id, lecturer_id=lecturer_id)
#         db.session.add(conversation)
#         db.session.commit()
#
#     new_message = Message(conversation_id=conversation.id, sender_id=student_id, message=message)
#     db.session.add(new_message)
#     db.session.commit()
#
#     emit('message', {'student_id': student_id, 'message': message}, room=lecturer_id)
# @app.route('/admin', methods=['GET', 'POST'])
# def admin_login():
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_dashboard'))
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = AdminUser.query.filter_by(username=username).first()
#
#         if user and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid username or password', 'error')
#
#     return render_template('admin_login.html')
#
# @app.route('/admin/logout')
# @login_required
# def admin_logout():
#     logout_user()
#     return redirect(url_for('admin_login'))

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





if __name__ == '__main__':
    db.create_all()
    socketio.run(app)
