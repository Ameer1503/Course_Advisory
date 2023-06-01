from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class StudentRegistrationForm(FlaskForm):
    matric_no = StringField('Matric Numbers', validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50)])
    level = SelectField('Level', choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')],validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LecturerRegistrationForm(FlaskForm):
    staff_id = StringField('Staff ID', validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')




class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class LecturerLoginForm(FlaskForm):
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class StudentLoginForm(FlaskForm):
    matric_no = StringField('Matric Numbers', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')