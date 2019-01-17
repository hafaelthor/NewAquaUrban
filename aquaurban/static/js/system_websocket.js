const SOCKET_HOST = 'http://192.168.0.12:5000';
const SYSTEM_NAMESPACE = '/system'
var system_websocket;

function on_bioinfo (bioinfo) {
	systemMinipanels[bioinfo.system_id].updateBioinfo(bioinfo);
}

function send_action (id, action, data) {
	system_websocket.emit('action', {id: id, action: action, data: data});
}

$(() => {
	system_websocket = io.connect(SOCKET_HOST + SYSTEM_NAMESPACE);
	system_websocket.on('bio', on_bioinfo);
});