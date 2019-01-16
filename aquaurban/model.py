from flask_login import UserMixin

from aquaurban import db, login_manager
from aquaurban.enum import ActionCode

@login_manager.user_loader
def load_user (user_id):
	return User.query.get(int(user_id))

class User (db.Model, UserMixin):
	id 			= db.Column(db.Integer, primary_key=True)
	username	= db.Column(db.String(20), unique=True, nullable=False)
	email	 	= db.Column(db.String(50), unique=True, nullable=False)
	password 	= db.Column(db.String(30), nullable=False)
	permission	= db.Column(db.SmallInteger, nullable=False)

	systems 	= db.relationship('System', backref='user', lazy=True)
	actions		= db.relationship('Action', backref='user', lazy=True)

	def __repr__ (self):
		return f'<USER {self.id} | username=\"{self.username}\" email=\"{self.email}\">'

class Community (db.Model):
	id 			= db.Column(db.Integer, primary_key=True)
	host 		= db.Column(db.String(40), nullable=False)
	port 		= db.Column(db.Integer, nullable=False)
	username 	= db.Column(db.String(20))
	password 	= db.Column(db.String(20))

	systems		= db.relationship('System', backref='community', lazy=True)

	def __repr__ (self):
		return f'<COMMUNITY {self.id} | {self.host}:{self.port}>'

class System (db.Model):
	id 				= db.Column(db.Integer, primary_key=True)
	name 			= db.Column(db.String(20), nullable=False)
	user_id			= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	community_id	= db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)

	bioinfos		= db.relationship('Bioinfo', backref='system', lazy=True)
	actions			= db.relationship('Action', backref='system', lazy=True)

	def __repr__ (self):
		return f'<SYSTEM {self.id} | name=\"{self.name}\">'

class Bioinfo (db.Model):
	id 			= db.Column(db.Integer, primary_key=True)
	timestamp	= db.Column(db.TIMESTAMP)
	waterlevel 	= db.Column(db.Boolean)
	brightness	= db.Column(db.Float)
	temperature = db.Column(db.Float)
	acidness	= db.Column(db.Float)
	system_id	= db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

	def __repr__ (self):
		return f'<BIOINFO {self.id} | [{"above" if self.waterlevel else "below"} {self.brightness}lm {self.temperature}ºC pH({self.acidness})] system_id={self.system_id}>'

class Action (db.Model):
	id 			= db.Column(db.Integer, primary_key=True)
	timestamp	= db.Column(db.TIMESTAMP)
	code		= db.Column(db.SmallInteger, nullable=False)
	data		= db.Column(db.SmallInteger)
	system_id 	= db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
	user_id 	= db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__ (self):
		if self.user_id: return f'<ACTION {self.id} | {ActionCode(self.code).name} system_id={self.system_id} user_id={self.user_id}>'
		else: return f'<ACTION {self.id} | {ActionCode(self.code).name} system_id={self.system_id} user_id=anonymous>'