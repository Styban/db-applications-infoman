from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, EmailField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Regexp


class StudentForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired()])
    middle_name = StringField('Middle name')
    last_name = StringField('Last name', validators=[InputRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[InputRequired()])
    gender = SelectField('Gender', choices=[
        ('M', 'Male'),
        ('F', 'Female')
    ], validators=[InputRequired()])
    civil_status = SelectField('Civil Status', choices=[
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('C', 'Civil Partnership'),
        ('O', 'Other')
    ], validators=[InputRequired()])
    phone = StringField('Phone number', validators=[InputRequired(), Regexp(
        r'^09\d{9}$', message='Invalid Philippine phone number')])
    email = EmailField('Email', validators=[Email(), InputRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[InputRequired()])
    submit = SubmitField('Submit')


class CourseForm(FlaskForm):
    course_name = StringField('Course name', validators=[InputRequired()])
    department = StringField('Department name', validators=[InputRequired()])
    submit = SubmitField('Submit')
