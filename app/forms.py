from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, URL, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    photo = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class ProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    parish = StringField('Parish', validators=[DataRequired(), Length(max=100)])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(max=1000)])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    race = StringField('Race', validators=[DataRequired(), Length(max=100)])
    birth_year = IntegerField('Birth Year', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    height = IntegerField('Height (in cm)', validators=[DataRequired(), NumberRange(min=100, max=300)])
    fav_cuisine = StringField('Favourite Cuisine', validators=[DataRequired(), Length(max=100)])
    fav_colour = StringField('Favourite Colour', validators=[DataRequired(), Length(max=50)])
    fav_school_subject = StringField('Favourite School Subject', validators=[DataRequired(), Length(max=100)])
    political = BooleanField('Political')
    religious = BooleanField('Religious')
    family_oriented = BooleanField('Family Oriented')
