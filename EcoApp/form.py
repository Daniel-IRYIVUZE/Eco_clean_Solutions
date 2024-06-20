from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from EcoApp.model import Users
from datetime import datetime

class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    district = StringField('District', validators=[DataRequired(), Length(min=2, max=20)])
    sector = StringField('Sector', validators=[DataRequired(), Length(min=2, max=20)])
    village = StringField('Village', validators=[DataRequired(), Length(min=2, max=20)])
    street = StringField('Street', validators=[Length(max=20)])
    cell = StringField('Cell', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken, please use another one")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ServiceForm(FlaskForm):
    serviceName = StringField('Service Name', validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])  # Changed to IntegerField
    date = DateField("Service Date", validators=[DataRequired()])
    submit = SubmitField("Book Order")

    def validate_date(self, date):
        if date.data < datetime.now().date():
            raise ValidationError("Date invalid, please select a future date")
