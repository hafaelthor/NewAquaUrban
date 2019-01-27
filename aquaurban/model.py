import time
from flask_login import UserMixin

from aquaurban import db, login_manager
from aquaurban.code import ActorCode, FEATURE_PERMISSION_TRESHOLD

@login_manager.user_loader
def load_user (user_id):
	return User.query.get(int(user_id))

class User (db.Model, UserMixin):
	id 				= db.Column(db.Integer, 	primary_key=True)
	username		= db.Column(db.String(20), 	unique=True, 	nullable=False)
	email	 		= db.Column(db.String(50), 	unique=True, 	nullable=False)
	password 		= db.Column(db.String(30), 					nullable=False)
	permission		= db.Column(db.SmallInteger, 				nullable=False)
	community_id	= db.Column(db.Integer, db.ForeignKey('community.id'))

	systems 		= db.relationship('System', backref='user', lazy=True)
	actions			= db.relationship('Action', backref='user', lazy=True)

	def __repr__ (self):
		return f'<USER {self.id} | username=\"{self.username}\" email=\"{self.email}\">'

class Community (db.Model):
	id 			= db.Column(db.Integer, 	primary_key=True)
	name		= db.Column(db.String(40), 	nullable=False)
	host 		= db.Column(db.String(40), 	nullable=False)
	port 		= db.Column(db.Integer, 	nullable=False)
	username 	= db.Column(db.String(20))
	password 	= db.Column(db.String(20))

	systems		= db.relationship('System', backref='community', lazy=True)
	supervisors = db.relationship('User', backref='community', lazy=True)

	def __repr__ (self):
		return f'<COMMUNITY {self.id} | {self.name} on {self.host}:{self.port}>'

class System (db.Model):
	id 				= db.Column(db.Integer, 								primary_key=True)
	name 			= db.Column(db.String(20), 								nullable=False)
	user_id			= db.Column(db.Integer, db.ForeignKey('user.id'), 		nullable=False)
	community_id	= db.Column(db.Integer, db.ForeignKey('community.id'), 	nullable=False)

	bioinfos		= db.relationship('Bioinfo', 	backref='system', lazy=True)
	actions			= db.relationship('Action', 	backref='system', lazy=True)

	def safe_ids_for (self, feature):
		ids = [self.user_id] + [supervisor.id for supervisor in self.community.supervisors]
		safe_ids  = []
		for unchecked_id in ids:
			if User.query.get(unchecked_id).permission >= FEATURE_PERMISSION_TRESHOLD[feature].value:
				safe_ids.append(unchecked_id)
		return safe_ids

	def __repr__ (self):
		return f'<SYSTEM {self.id} | name=\"{self.name}\">'

class Bioinfo (db.Model):
	id 			= db.Column(db.Integer, primary_key=True)
	timestamp	= db.Column(db.TIMESTAMP)
	waterlevel 	= db.Column(db.Boolean)
	brightness	= db.Column(db.Float)
	temperature = db.Column(db.Float)
	humidity	= db.Column(db.Float)
	acidness	= db.Column(db.Float)
	system_id	= db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

	def to_dict (self):
		return {
			"timestamp": time.mktime(self.timestamp.timetuple()),
			"waterlevel": self.waterlevel,
			"brightness": self.brightness,
			"temperature": self.temperature,
			"humidity": self.humidity,
			"acidness": self.acidness,
			"system_id": self.system_id
		}

	def __repr__ (self):
		return f'<BIOINFO {self.id} | [{"above" if self.waterlevel else "below"} {self.brightness}lm {self.temperature}ºC {self.humidity}% pH({self.acidness}) at {self.timestamp}] system_id={self.system_id}>'

class Action (db.Model):
	id 			= db.Column(db.Integer, 							primary_key=True)
	timestamp	= db.Column(db.TIMESTAMP)
	actor		= db.Column(db.SmallInteger, 						nullable=False)
	info		= db.Column(db.Integer)
	system_id 	= db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
	user_id 	= db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__ (self):
		if self.user_id: return f'<ACTION {self.id} | [{ActorCode(self.actor).name}({self.info}) at {self.timestamp}] system_id={self.system_id} user_id={self.user_id}>'
		else: return f'<AUTOACTION {self.id} | [{ActorCode(self.actor).name}({self.info}) at {self.timestamp}] system_id={self.system_id}>'