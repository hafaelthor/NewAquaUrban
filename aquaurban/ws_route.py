from flask import request
from flask_login import current_user
import datetime

import aquaurban
from aquaurban import db
from aquaurban.code import ActorCode
from aquaurban import socketio
from aquaurban.model import System, Action

sids = dict()

@socketio.on('connect', namespace='/system')
def handle_connect ():
	global sids
	print('- system websocket connect')
	print(f'\t- sid: 		{request.sid}')
	print(f'\t- user.id:	{current_user.id}')
	sids[current_user.id] = request.sid

@socketio.on('action', namespace='/system')
def handle_action (data):
	system_id	= data["id"]
	system 		= System.query.get(system_id)
	if current_user.id not in system.safe_ids_for('act'): return False
	actor 		= data["actor"]
	info		= data["info"]
	timestamp	= data["timestamp"]
	action = Action(system_id=system_id, timestamp=datetime.datetime.fromtimestamp(timestamp), actor=actor, info=info, user_id=current_user.id)
	db.session.add(action)
	db.session.commit()
	aquaurban.mqtt_hub.send_action(system, ActorCode(actor), info)

def send_bioinfo (bioinfo):
	for safe_id in bioinfo.system.safe_ids_for('bio') & sids.keys():
		socketio.emit('bio', bioinfo.to_dict(), room=sids[safe_id], namespace='/system')