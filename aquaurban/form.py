from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from aquaurban.model import User

class RegistrationForm (FlaskForm):
	username 	= StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email 		= StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
	password 	= PasswordField('Password', validators=[DataRequired(), Length(max=30)])
	cpassword	= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	as_dummy	= BooleanField('As Dummy?')
	submit 		= SubmitField('Sign Up')

	def validate_username (self, username):
		if db.session.query(User).filter_by(username=username.data).first():
			raise ValidationError('Username already taken. Choose another.')

	def validate_email (self, email):
		if db.session.query(User).filter_by(email=email.data).first():
			raise ValidationError('E-mail already taken. Choose another.')

class LoginForm (FlaskForm):
	email 		= StringField('Email', validators=[DataRequired(), Email()])
	password 	= PasswordField('Password', validators=[DataRequired()])
	remember 	= BooleanField('Remember Me')
	submit 		= SubmitField('Login')

class CreateSystemForm (FlaskForm):
	name		= StringField('System Name', validators=[DataRequired(), Length(max=20)])
	community	= SelectField('Community', coerce=int)
	user_pass	= PasswordField('User Password', validators=[DataRequired()])
	submit 		= SubmitField('Create')