import base64
import os

from flask import redirect, url_for, session, abort
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_admin.form import FileUploadField, rules
from flask_login import current_user, LoginManager, login_required
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import TextAreaField, PasswordField
from wtforms.widgets import TextArea

import app

# class SecureModelView(ModelView):
#     def is_accessible(self):
#         if "logged in" in session:
#             return True
#         else:
#             abort(403)
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
        'level': 'Level',
        'profile_image': 'Profile Image'
    }

    # Set the column filters to be displayed in the list view
    column_filters = ['matric_no', 'email', 'level']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['matric_no', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['matric_no', 'firstname', 'lastname', 'email', 'level', 'password', 'profile_image' ]
    form_choices = {
        'level': level_choices
    }

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'matric_no': 'Matric Number',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'password': 'Password',
        'profile_image': 'Profile Image'
    }

    # Set the form field types for profile_image
    form_extra_fields = {
        'profile_image': FileUploadField('Profile Image', base_path='static/images/students')
    }

    form_overrides = {
        'password': PasswordField,
        'profile_image': FileUploadField
    }

    form_widget_args = {
        'password': {
            'autocomplete': 'new-password',  # Prevent browser autofill
            'class': 'password-field'  # Apply a CSS class to the password field
        }
    }

    form_rules = [
        rules.FieldSet(('matric_no', 'firstname', 'lastname', 'email', 'level', 'profile_image'),
                       'Student Information'),
        rules.Field('password')
    ]

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)
        else:
            del model.password  # Remove the password field from the update if it's empty




class LecturerAdmin(ModelView):
    # Set the column labels to be displayed in the list view
    column_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'profile_image': 'Profile Image'

    }

    # Set the column filters to be displayed in the list view
    column_filters = ['staff_id', 'email']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['staff_id', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['staff_id', 'firstname', 'lastname', 'email', 'password', 'profile_image']

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'password': 'Password',
        'profile_image': 'Profile Image'
    }

    # Set the form field types for profile_image
    form_extra_fields = {
        'profile_image': FileUploadField('Profile Image', base_path='static/images/lecturers')
    }

    form_overrides = {
        'password': PasswordField,
        'profile_image': FileUploadField
    }

    form_widget_args = {
        'password': {
            'autocomplete': 'new-password',  # Prevent browser autofill
            'class': 'password-field'  # Apply a CSS class to the password field
        }
    }

    form_rules = [
        rules.FieldSet(('staff_id', 'firstname', 'lastname', 'email', 'profile_image'),
                       'Lecturer Information'),
        rules.Field('password')
    ]
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)



class ChatAdmin(ModelView):
    # Customize the displayed columns, search fields, and filters if needed
    column_list = ['id', 'sender', 'receiver', 'message', 'timestamp']
    column_searchable_list = ['id','sender']
    column_filters = ['receiver', 'sender']

class FAQAdmin(ModelView):
    column_list = ['id','question', 'answer']
    column_searchable_list = ['id']

    form_columns = ['question', 'answer']

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'question': 'Question',
        'answer': 'Answer',
    }

    form_overrides = {
        'answer': TextAreaField
    }

    def on_model_change(self, form, model, is_created):
        model.answer = model.answer.replace('\r\n', '<br>')

    def scaffold_form(self):
        form_class = super(FAQAdmin, self).scaffold_form()
        form_class.answer.widget = TextArea()
        return form_class


class OpinionAdmin(ModelView):
    column_list = ['id','profession', 'answer']
    column_searchable_list = ['id']

    form_columns = ['profession', 'answer']

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'profession': 'Question',
        'answer': 'Answer',
    }

    form_overrides = {
        'answer': TextAreaField
    }

    def on_model_change(self, form, model, is_created):
        model.answer = model.answer.replace('\r\n', '<br>')

    def scaffold_form(self):
        form_class = super(OpinionAdmin, self).scaffold_form()
        form_class.answer.widget = TextArea()
        return form_class