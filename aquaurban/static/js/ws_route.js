const SOCKET_HOST = 'http://192.168.0.12:5000';
var socket;

function on_bioinfo (bioinfo) {
	var systemId = bioinfo.id
	systemMinipanels[systemId].updateBioinfo(bioinfo);
}

function send_action (id, action) {
	socket.emit('action', {id: id, action: action});
}

$(() => {
	socket = io.connect(SOCKET_HOST);

	socket.on('bio', on_bioinfo);
});