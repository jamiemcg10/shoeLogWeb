from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Activity
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The username you entered is already in use. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('The email address you entered is already in use. Please use a different email address.')

class LogRunForm(FlaskForm):
    date = DateField('Date of run', format='%m-%d-%y', default=date.today())
    walk = DecimalField('Miles walked')
    run = DecimalField('Miles run')
    shoe = StringField('Shoes worn', validators=[DataRequired()])
    type = StringField('Run type')
    submit = SubmitField('Upload')
    
    
class ShoeCalcForm(FlaskForm):
    total_mi = '-'
    walk_mi = '-'
    run_mi = '-'

    temp_shoes = Activity.query.distinct(Activity.shoe).group_by(Activity.shoe)
    shoes = []
    i = 0
    for shoe in temp_shoes:
        shoes.append((str(i), shoe.shoe))
        i+=1
    shoe = SelectField('Select shoe: ', choices=shoes)
    submit = SubmitField('Calculate')