# NewAquaUrban

A program for network control of aquaponic systems.

## The Main Blueprint

### System
Aquaponic systems will read biological information and perform actions. The system will listening for instructions while sending biological information using the mqtt protocol if it has a wireless hotspot. To improve homeostasis, it will act in the system keeping biological factors steady.

### Community

Communities will be hosted as brokers that will intermediate the communication between systems and users. In each community will be controlled by supervisors that will have open access to all systems inside a community.

### User and Supervisor
Users will have different permissions to act in the system, from those who can only read, to major supervisors who will have complete access to all systems inside a given community and it's subcommunities.

## Main APIs and Packages

### Flask
- http serving with user authentication
- including flask_login, flask_bcrypt and jinja templating

### Socket.IO
- websocket functionality for real time communication
- using as flask_socketio in the server

### SQL Alchemy
- database handling

### Paho MQTT
- mqtt communication with different systems

## Communication Funcionality

- (html, js, css)			user <- httpserver
- (bioinfo and actions)	user <-> wsserver <-> mqttclient(in server) <-> broker <-> mqttclient(in system)
