from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_babel import Babel
import aquaurban

app = Flask(__name__)
app.config.from_object('config.mqtt_dev')
app.add_template_global(aquaurban, 'aquaurban')
'''
THE CONFIG DIRECTORY IS IN THE ROOT DIRECTORY AND IGNORED BY GIT FOR SECURITY.
TO MAKE THE APP RUN, CREATE YOUR OWN CONFIG PACKAGE OR DO AS YOU LIKE...
see: http://exploreflask.com/en/latest/configuration.html
'''
db = SQLAlchemy(app)
'''
TO USE THE DATABASE WITH SQLALCHEMY, YOU NEED TO ADD A CONFIG VARIABLE
CALLED "SQLALCHEMY_DATABASE_URI" WITH THE FILEPATH RELATIVE TO THE
"aquaurban" PACKAGE FOLDER.
and you should run "db.create_all()" to create the database with all tables
'''
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
socketio = SocketIO(app, async_mode='threading')
babel = Babel(app)
'''
THE CONFIGURATION USED BY BABEL IS IN THE KEY "BABEL_DEFAULT_LOCALE"
WICH STORES THE DEFAULT LOCALE, SUCH AS 'en', etc. 

TO USE/UPDATE THE TRANSLATIONS, YOU NEED TO USE THE FOLLOWING INSTRUCTIONS IN THE "NewAquaUrban/" FOLDER:
pybabel extract -F aquaurban/babel.cfg -o aquaurban/messages.pot . 			#register in "aquaurban/messages.pot" all gettext() in python and _() in jinja2
pybabel init -i aquaurban/messages.pot -d aquaurban/translations -l pt 		#initialize a portuguese (pt) translation text file
pybabel update -i aquaurban/messages.pot -d aquaurban/translations -l pt 	#update a portuguese (pt) translation text file
pybabel compile -d aquaurban/translations 									#compile all translations into binary files

IF ON A LINUX SYSTEM, SIMPLY RUN:
sh babel-register.sh
sh babel-compile.sh
'''

from aquaurban import http_route, ws_route
from aquaurban.mqtt_route import MqttHub
mqtt_hub = MqttHub()