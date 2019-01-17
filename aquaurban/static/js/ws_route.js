const SOCKET_HOST = 'http://192.168.0.12:5000';
const SYSTEM_NAMESPACE = '/system'
var system_socket;

function on_bioinfo (bioinfo) {
	systemMinipanels[bioinfo.system_id].updateBioinfo(bioinfo);
}

function send_action (id, action) {
	system_socket.emit('action', {id: id, action: action});
}

$(() => {
	system_socket = io.connect(SOCKET_HOST + SYSTEM_NAMESPACE);
	system_socket.on('bio', on_bioinfo);
});