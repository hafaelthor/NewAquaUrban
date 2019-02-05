from flask_babel import lazy_gettext

class FLASH_CLASS:
	REGISTER_ERROR_LOGGED_IN = lazy_gettext('You\'re already logged in. To register, first logout.')
	REGISTER_ERROR_LOGGED_IN_CATEGORY = 'danger'
	REGISTER_SUCCESS = lambda self, username: lazy_gettext('%(user)s Account created!', user=username)
	REGISTER_SUCCESS_CATEGORY = 'success'
	
	LOGIN_ERROR_LOGGED_IN = lazy_gettext('You\'re already logged in. To switch user, first logout.')
	LOGIN_ERROR_LOGGED_IN_CATEGORY = 'danger'
	LOGIN_ERROR_WRONG_PASSWORD = lazy_gettext('Wrong password. Try again.')
	LOGIN_ERROR_WRONG_PASSWORD_CATEGORY = 'danger'
	LOGIN_ERROR_WRONG_EMAIL = lazy_gettext('E-Mail not known. Try again.')
	LOGIN_ERROR_WRONG_EMAIL_CATEGORY = 'danger'
	LOGIN_SUCCESS = lazy_gettext('Login successful!')
	LOGIN_SUCCESS_CATEGORY = 'success'
	
	LOGOUT_SUCCESS = lazy_gettext('Logout successful!')
	LOGOUT_SUCCESS_CATEGORY = 'success'
	
	SYSREGISTER_SUCCESS = lazy_gettext('System registered succesfully')
	SYSREGISTER_SUCCESS_CATEGORY = 'success'
	SYSREGISTER_ERROR_USED_NAME = lazy_gettext('You already used that name in other system. Use another.')
	SYSREGISTER_ERROR_USED_NAME_CATEGORY = 'danger'
	SYSREGISTER_ERROR_WRONG_PASSWORD = lazy_gettext('Wrong password. Try again.')
	SYSREGISTER_ERROR_WRONG_PASSWORD_CATEGORY = 'danger'

FLASH = FLASH_CLASS()

class VALIDATE_ERROR_CLASS:
	REGISTER_ERROR_USERNAME_REQUIRED = lazy_gettext('Username is required.')
	REGISTER_ERROR_USERNAME_LENGTH = lazy_gettext('Username or too short or too long. Choose another.')
	REGISTER_ERROR_USED_USERNAME = lazy_gettext('Username already taken. Choose another.')
	REGISTER_ERROR_EMAIL_REQUIRED = lazy_gettext('E-mail is required.')
	REGISTER_ERROR_EMAIL_FORMAT = lazy_gettext('Invalid E-mail.')
	REGISTER_ERROR_EMAIL_LENGTH = lazy_gettext('E-mail is too long. Chose another.')
	REGISTER_ERROR_USED_EMAIL = lazy_gettext('E-mail already taken. Choose another.')
	REGISTER_ERROR_PASSWORD_REQUIRED = lazy_gettext('Password is required.')
	REGISTER_ERROR_PASSWORD_LENGTH = lazy_gettext('Password too long. Choose another.')
	REGISTER_ERROR_CPASSWORD_REQUIRED = lazy_gettext('Confirm password.')
	REGISTER_ERROR_CPASSWORD_UNEQUAL = lazy_gettext('The passwords don\'t match.')

VALIDATE_ERROR = VALIDATE_ERROR_CLASS()