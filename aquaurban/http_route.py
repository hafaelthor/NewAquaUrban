from flask import render_template, send_from_directory, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

import aquaurban
from aquaurban import app, db, bcrypt
from aquaurban.code import UserPermissionCode
from aquaurban.model import User, Community, System
from aquaurban.form import RegistrationForm, LoginForm, CreateSystemForm
#from aquaurban.mqtt_route import listen_system

@app.route('/')
def index ():
	return render_template('index.html')

@app.route('/about')
def about ():
	return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register ():
	if current_user.is_authenticated and request.method == 'GET':
		flash('You\'re already logged in. To register, first logout.', 'danger')
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		db.session.add(User(username=form.username.data, email=form.email.data, password=pw_hash, 
			permission=UserPermissionCode.COMMON.value if not form.as_dummy.data else UserPermissionCode.DUMMY.value))
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login ():
	if current_user.is_authenticated:
		flash('You\'re already logged in. To switch user, first logout.', 'danger')
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				next_url = request.args.get('next')
				flash('Login successful!', 'success')
				return redirect(next_url) if next_url else redirect(url_for('index'))
			else: flash('Wrong password. Try again.', 'danger')
		else: flash('E-Mail not known. Try again.', 'danger')
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout ():
	logout_user()
	flash('Logout successful!', 'success')
	return redirect(url_for('index'))

@app.route('/account')
@login_required
def account ():
	return render_template('account.html')

@app.route('/system/create', methods=['GET', 'POST'])
@login_required
def create_system ():
	form = CreateSystemForm()
	form.community.choices = [(comm.id, f'{comm.host}:{comm.port}') for comm in Community.query.all()]
	if form.validate_on_submit():
		if bcrypt.check_password_hash(current_user.password, form.user_pass.data):
			if not System.query.filter_by(user_id=current_user.id, name=form.name.data).first():
				system = System(name=form.name.data, user_id=current_user.id, community_id=form.community.data)
				db.session.add(system)
				db.session.commit()
				aquaurban.mqtt_hub.listen_system(system)
				flash('System registered succesfully', 'success')
				return redirect(url_for('index'))
			else: flash('You already used that name in other system. Use another.', 'danger')
		else: flash('Wrong password. Try again.', 'danger')
	return render_template('system/create.html', form=form)

@app.route('/system/dashboard')
@login_required
def system_dashboard ():
	return render_template('system/dashboard.html')