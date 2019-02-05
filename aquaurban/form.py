from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from aquaurban import db
from aquaurban.quick_message import VALIDATE_ERROR
from aquaurban.model import User

class RegistrationForm (FlaskForm):
	username = StringField(lazy_gettext('Username'), validators=[
		DataRequired(message=VALIDATE_ERROR.REGISTER_ERROR_USERNAME_REQUIRED), 
		Length(message=VALIDATE_ERROR.REGISTER_ERROR_USERNAME_LENGTH, min=2, max=20)])
	email = StringField(lazy_gettext('Email'), validators=[
		DataRequired(message=VALIDATE_ERROR.REGISTER_ERROR_EMAIL_REQUIRED), 
		Email(message=VALIDATE_ERROR.REGISTER_ERROR_EMAIL_FORMAT), 
		Length(message=VALIDATE_ERROR.REGISTER_ERROR_EMAIL_LENGTH, max=50)])
	password = PasswordField(lazy_gettext('Password'), validators=[
		DataRequired(message=VALIDATE_ERROR.REGISTER_ERROR_PASSWORD_REQUIRED), 
		Length(message=VALIDATE_ERROR.REGISTER_ERROR_PASSWORD_LENGTH, max=30)])
	cpassword = PasswordField(lazy_gettext('Confirm Password'), validators=[
		DataRequired(message=VALIDATE_ERROR.REGISTER_ERROR_CPASSWORD_REQUIRED), 
		EqualTo('password', message=VALIDATE_ERROR.REGISTER_ERROR_CPASSWORD_UNEQUAL)])
	as_dummy = BooleanField(lazy_gettext('As Dummy?'))
	submit = SubmitField(lazy_gettext('Sign Up'))

	def validate_username (self, username):
		if db.session.query(User).filter_by(username=username.data).first():
			raise ValidationError(VALIDATE_ERROR.REGISTER_ERROR_USED_USERNAME)

	def validate_email (self, email):
		if db.session.query(User).filter_by(email=email.data).first():
			raise ValidationError(VALIDATE_ERROR.REGISTER_ERROR_USED_EMAIL)

class LoginForm (FlaskForm):
	email 		= StringField(lazy_gettext('Email'), validators=[DataRequired(), Email()])
	password 	= PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
	remember 	= BooleanField(lazy_gettext('Remember Me'))
	submit 		= SubmitField(lazy_gettext('Login'))

class CreateSystemForm (FlaskForm):
	name		= StringField(lazy_gettext('System Name'), validators=[DataRequired(), Length(max=20)])
	community	= SelectField(lazy_gettext('Community'), coerce=int)
	user_pass	= PasswordField(lazy_gettext('User Password'), validators=[DataRequired()])
	submit 		= SubmitField(lazy_gettext('Register'))