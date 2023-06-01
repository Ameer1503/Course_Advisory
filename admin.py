from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import Student, Lecturer
import app
from database import db

 # Add more ModelViews for other models if needed

level_choices = [
    ('100', '100'),
    ('200', '200'),
    ('300', '300'),
    ('400', '400')
]
class StudentAdmin(ModelView):
    # Set the column labels to be displayed in the list view
    column_labels = {
        'matric_no': 'Matric Number',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'level': 'Level'
    }

    # Set the column filters to be displayed in the list view
    column_filters = ['matric_no', 'email', 'level']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['matric_no', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['matric_no', 'firstname', 'lastname', 'email', 'level' ]
    form_choices = {
        'level': level_choices
    }

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'matric_no': 'Matric Number',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
    }


class LecturerAdmin(ModelView):
    # Set the column labels to be displayed in the list view
    column_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
    }

    # Set the column filters to be displayed in the list view
    column_filters = ['staff_id', 'email']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['staff_id', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['staff_id', 'firstname', 'lastname', 'email']

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
    }

class ConversationAdminView(ModelView):
    # Customize the displayed columns, search fields, and filters if needed
    column_list = ['id', 'student_id', 'lecturer_id']
    column_searchable_list = ['id']
    column_filters = ['student_id', 'lecturer_id']

class MessageAdminView(ModelView):
    # Customize the displayed columns, search fields, and filters if needed
    column_list = ['id', 'conversation_id', 'sender_id', 'message', 'timestamp']
    column_searchable_list = ['id', 'conversation_id']
    column_filters = ['conversation_id', 'sender_id', 'timestamp']
