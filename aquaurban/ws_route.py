from flask import request
from flask_login import current_user
from flask_socketio import Namespace

import aquaurban
from aquaurban.code import ActionCode
from aquaurban import socketio
from aquaurban.model import System

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
	system = System.query.get(data["id"])
	action = data["action"]
	if current_user.id not in system.safe_ids_for('act'): return False
	else: aquaurban.mqtt_hub.send_action(system, ActionCode(action))

def send_bioinfo (bioinfo):
	for safe_id in bioinfo.system.safe_ids_for('bio') & sids.keys():
		socketio.emit('bio', bioinfo.to_dict(), room=sids[safe_id], namespace='/system')