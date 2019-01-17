from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '6dedf2697cbad5516fa43f98d18c4499'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
socketio = SocketIO(app, async_mode='threading')

from aquaurban import model, enum, http_route, ws_route
from aquaurban.mqtt_route import MqttHub
mqtt_hub = MqttHub()
#def send_action (system, action):
#	mqtt_send_action(system, ActionCode(action))

#from aquaurban.mqtt_route import setup, mqtt_connections, send_action as mqtt_send_action
#from aquaurban import http_route,  ws_route
#from aquaurban.model import User, Community, System
#from aquaurban.enum import ActionCode

#setup()

#comm = Community(host='m15.cloudmqtt.com', port=14689, username='mabrghbp', password='DY-djqEBxfAy')