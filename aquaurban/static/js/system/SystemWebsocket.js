class SystemWebsocket {
	constructor (host) {
		this.namespace = '/system';

		this.socket = io.connect(host + this.namespace);
		this.socket.on('bio', this.on_bioinfo);
	}

	on_bioinfo (bio) {
		systemMinipanels[bio.system_id].updateBioinfo(bio);
	}

	send_action (id, actor, info, timestamp) {
		this.socket.emit('action', 
			{id: id, actor: actor, info: info, timestamp: timestamp});
	}

	send_setting (id, setting, info) {
		this.socket.emit('setting', 
			{id: id, setting: setting, info: info});
	}
}