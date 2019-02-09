from flask import render_template, send_from_directory, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt

import aquaurban
from aquaurban import app, db, babel
from aquaurban.quick_message import FLASH
from aquaurban.code import UserPermissionCode
from aquaurban.model import User, Community, System, Bioinfo
from aquaurban.form import RegistrationForm, LoginForm, CreateSystemForm

AVAILABLE_LOCALES = ['en', 'pt']

@babel.localeselector
def get_locale ():
	return request.accept_languages.best_match(AVAILABLE_LOCALES)

'''*************

TEMPLATE ROUTING

*************'''

@app.route('/')
def index ():
	return render_template('index.html')

@app.route('/about')
def about ():
	return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register ():
	if current_user.is_authenticated and request.method == 'GET':
		flash(FLASH.REGISTER_ERROR_LOGGED_IN, FLASH.REGISTER_ERROR_LOGGED_IN_CATEGORY)
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt()).decode()
		db.session.add(User(username=form.username.data, email=form.email.data, password=pw_hash, 
			permission=UserPermissionCode.COMMON.value if not form.as_dummy.data else UserPermissionCode.DUMMY.value))
		db.session.commit()
		flash(FLASH.REGISTER_SUCCESS(form.username.data), FLASH.REGISTER_SUCCESS_CATEGORY)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login ():
	if current_user.is_authenticated:
		flash(FLASH.LOGIN_ERROR_LOGGED_IN, FLASH.LOGIN_ERROR_LOGGED_IN_CATEGORY)
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter_by(email=form.email.data).first()
		if user:
			if bcrypt.hashpw(form.password.data.encode(), user.password.encode()) == user.password.encode():
				login_user(user, remember=form.remember.data)
				next_url = request.args.get('next')
				flash(FLASH.LOGIN_SUCCESS, FLASH.LOGIN_SUCCESS_CATEGORY)
				return redirect(next_url) if next_url else redirect(url_for('index'))
			else: flash(FLASH.LOGIN_ERROR_WRONG_PASSWORD, FLASH.LOGIN_ERROR_WRONG_PASSWORD_CATEGORY)
		else: flash(FLASH.LOGIN_ERROR_WRONG_EMAIL, FLASH.LOGIN_ERROR_WRONG_EMAIL_CATEGORY)
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

@app.route('/system/register', methods=['GET', 'POST'])
@login_required
def register_system ():
	form = CreateSystemForm()
	form.community.choices = [(comm.id, comm.name) for comm in db.session.query(Community).all()]
	if form.validate_on_submit():
		if bcrypt.hashpw(form.user_pass.data.encode(), current_user.password.encode()) == current_user.password.encode():
			if not db.session.query(System).filter_by(user_id=current_user.id, name=form.name.data).first():
				system = System(name=form.name.data, user_id=current_user.id, community_id=form.community.data)
				db.session.add(system)
				db.session.commit()
				aquaurban.mqtt_hub.listen_system(system)
				flash(FLASH.SYSREGISTER_SUCCESS, FLASH.SYSREGISTER_SUCCESS_CATEGORY)
				return redirect(url_for('index'))
			else: flash(FLASH.SYSREGISTER_ERROR_USED_NAME, FLASH.SYSREGISTER_ERROR_USED_NAME_CATEGORY)
		else: flash(FLASH.SYSREGISTER_ERROR_WRONG_PASSWORD, FLASH.SYSREGISTER_ERROR_WRONG_PASSWORD_CATEGORY)
	return render_template('system/register.html', form=form)

@app.route('/system/dashboard')
@login_required
def system_dashboard ():
	return render_template('system/dashboard.html')

'''*********

JSON ROUTING

*********'''

from datetime import datetime

@app.route('/system/hquery/<int:system_id>')
def system_hquery (system_id):
	system = db.session.query(System).get(system_id)
	data = {
		"timestamp": [],
		"waterlevel": [],
		"brightness": [],
		"temperature": [],
		"humidity": [],
		"acidness": []
	}
	try:
		ti = int(request.args.get('ti'))
		tf = int(request.args.get('tf'))
		for bio in db.session.query(Bioinfo).filter(
			Bioinfo.system_id == system_id, Bioinfo.timestamp >= ti, Bioinfo.timestamp <= tf).all():
			data["timestamp"].append(bio.timestamp)
			data["waterlevel"].append(bio.waterlevel)
			data["brightness"].append(bio.brightness)
			data["temperature"].append(bio.temperature)
			data["humidity"].append(bio.humidity)
			data["acidness"].append(bio.acidness)
	except Exception as err:
		return jsonify({"error": "Error during query"})
	return jsonify(data)

@app.route('/system/hlast/<int:system_id>')
def system_hlast (system_id):
	system = db.session.query(System).get(system_id)
	data = {
		"timestamp": [],
		"waterlevel": [],
		"brightness": [],
		"temperature": [],
		"humidity": [],
		"acidness": []
	}
	for bio in db.session.query(Bioinfo).filter(Bioinfo.system_id == system_id).all()[-5:]:
		data["timestamp"].append(bio.timestamp)
		data["waterlevel"].append(bio.waterlevel)
		data["brightness"].append(bio.brightness)
		data["temperature"].append(bio.temperature)
		data["humidity"].append(bio.humidity)
		data["acidness"].append(bio.acidness)
	return jsonify(data)