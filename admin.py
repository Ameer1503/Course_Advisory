import base64
import os

from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_admin.form import FileUploadField
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import TextAreaField
from wtforms.widgets import TextArea

import app

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
        'image': 'Image',
    }

    # Set the column filters to be displayed in the list view
    column_filters = ['matric_no', 'email', 'level']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['matric_no', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['matric_no', 'firstname', 'lastname', 'email', 'level', 'image', 'password' ]
    form_choices = {
        'level': level_choices
    }

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'matric_no': 'Matric Number',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'image': 'Image',
        'password': 'Password'
    }

    form_overrides = {
        'image': FileUploadField
    }

    form_args = {
        'image': {
            'label': 'Image',
            'base_path': '/static/images/student' # Path to save uploaded images

        }
    }

    def on_model_change(self, form, model, is_created):
        image_file = form.image.data
        if image_file:
            image_data = image_file.read()
            model.image = base64.b64encode(image_data)

            print('Image saved:', model.image)  # Add this line to check the image data

            # Save the file to the specified path
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)

            print('Image saved at:', file_path)  # Add this line to check the saved path


        super(StudentAdmin, self).on_model_change(form, model, is_created)


class LecturerAdmin(ModelView):
    # Set the column labels to be displayed in the list view
    column_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'image': 'Image',

    }

    # Set the column filters to be displayed in the list view
    column_filters = ['staff_id', 'email']

    # Set the column search options to be displayed in the list view
    column_searchable_list = ['staff_id', 'email']

    # Set the form fields to be displayed in the create/edit views
    form_columns = ['staff_id', 'firstname', 'lastname', 'email', 'image', 'password']

    # Set the form field labels to be displayed in the create/edit views
    form_labels = {
        'staff_id': 'Staff ID',
        'firstname': 'First Name',
        'lastname': 'Last Name',
        'email': 'Email',
        'image': 'Image',
        'password': 'Password'
    }

    form_overrides = {
        'image': FileUploadField
    }

    form_args = {
        'image': {
            'label': 'Image',
            'base_path': '/static/images/lecturer'  # Path to save uploaded images
        }
    }

    def on_model_change(self, form, model, is_created):
        image_file = form.image.data
        if image_file:
            image_data = image_file.read()
            model.image = base64.b64encode(image_data)

            print('Image saved:', model.image)  # Add this line to check the image data

            # Save the file to the specified path
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)

            print('Image saved at:', file_path)  # Add this line to check the saved path

        super(LecturerAdmin, self).on_model_change(form, model, is_created)


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