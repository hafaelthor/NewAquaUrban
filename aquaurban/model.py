import time
from sqlalchemy import Column, ForeignKey
from sqlalchemy import SmallInteger, Integer, BigInteger, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin

from aquaurban import db, login_manager
from aquaurban.code import ActorCode, FEATURE_PERMISSION_TRESHOLD

Base = declarative_base()

@login_manager.user_loader
def load_user (user_id):
	return db.session.query(User).get(int(user_id))

class User (Base, UserMixin):
	__tablename__ = 'user'

	id 				= Column(Integer, 	primary_key=True)
	username		= Column(String(20), unique=True, 	nullable=False)
	email	 		= Column(String(50), unique=True, 	nullable=False)
	password 		= Column(String(30), 				nullable=False)
	permission		= Column(SmallInteger, 				nullable=False)
	community_id	= Column(Integer, ForeignKey('community.id'))

	systems 		= relationship('System', backref='user', lazy=True)
	actions			= relationship('Action', backref='user', lazy=True)

	def __repr__ (self):
		return f'<USER {self.id} | username=\"{self.username}\" email=\"{self.email}\">'

class Community (Base):
	__tablename__ = 'community'

	id 			= Column(Integer, 	primary_key=True)
	name		= Column(String(40), nullable=False)
	host 		= Column(String(40), nullable=False)
	port 		= Column(Integer, 	nullable=False)
	username 	= Column(String(20))
	password 	= Column(String(20))

	systems		= relationship('System', backref='community', lazy=True)
	supervisors = relationship('User', backref='community', lazy=True)

	def __repr__ (self):
		return f'<COMMUNITY {self.id} | {self.name} on {self.host}:{self.port}>'

class System (Base):
	__tablename__ = 'system'

	id 				= Column(Integer, 								primary_key=True)
	name 			= Column(String(20), 							nullable=False)
	user_id			= Column(Integer, ForeignKey('user.id'), 		nullable=False)
	community_id	= Column(Integer, ForeignKey('community.id'), 	nullable=False)

	bioinfos		= relationship('Bioinfo', 	backref='system', lazy=True)
	actions			= relationship('Action', 	backref='system', lazy=True)

	def safe_ids_for (self, feature):
		ids = [self.user_id] + [supervisor.id for supervisor in self.community.supervisors]
		safe_ids  = []
		for unchecked_id in ids:
			if db.session.query(User).get(unchecked_id).permission >= FEATURE_PERMISSION_TRESHOLD[feature].value:
				safe_ids.append(unchecked_id)
		return safe_ids

	def __repr__ (self):
		return f'<SYSTEM {self.id} | name=\"{self.name}\">'

class Bioinfo (Base):
	__tablename__ = 'bioinfo'

	id 			= Column(Integer, primary_key=True)
	timestamp	= Column(BigInteger)
	waterlevel 	= Column(Boolean)
	brightness	= Column(Float)
	temperature = Column(Float)
	humidity	= Column(Float)
	acidness	= Column(Float)
	system_id	= Column(Integer, ForeignKey('system.id'), nullable=False)

	def to_dict (self):
		return {
			"timestamp": 	self.timestamp,
			"waterlevel": 	self.waterlevel,
			"brightness": 	self.brightness,
			"temperature": 	self.temperature,
			"humidity": 	self.humidity,
			"acidness": 	self.acidness,
			"system_id": 	self.system_id
		}

	def __repr__ (self):
		return f'<BIOINFO {self.id} | [{"above" if self.waterlevel else "below"} {self.brightness}lm {self.temperature}ºC {self.humidity}% pH({self.acidness}) at {self.timestamp}] system_id={self.system_id}>'

class Action (Base):
	__tablename__ = 'action'

	id 			= Column(Integer, 							primary_key=True)
	timestamp	= Column(BigInteger)
	actor		= Column(SmallInteger, 						nullable=False)
	info		= Column(Integer)
	system_id 	= Column(Integer, ForeignKey('system.id'), 	nullable=False)
	user_id 	= Column(Integer, ForeignKey('user.id'))

	def __repr__ (self):
		if self.user_id: return f'<ACTION {self.id} | [{ActorCode(self.actor).name}({self.info}) at {self.timestamp}] system_id={self.system_id} user_id={self.user_id}>'
		else: return f'<AUTOACTION {self.id} | [{ActorCode(self.actor).name}({self.info}) at {self.timestamp}] system_id={self.system_id}>'