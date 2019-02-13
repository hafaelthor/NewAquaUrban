const SOCKET_HOST = 'http://127.0.0.1:8181';
var systemMinipanels = {}, 
	systemWebsocket;

$(() => {
	$('.system-minipanel').each(function () {
		systemMinipanels[$(this).data('system-id')] = new SystemMinipanel($(this).data('id'));
	});
	systemWebsocket = new SystemWebsocket(SOCKET_HOST);
});