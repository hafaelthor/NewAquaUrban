class SystemMinipanel {
	constructor (id) {
		this.$minipanel = $('.system-minipanel[data-id="' + id + '"]').first();
		this.$bioinfo 	= {};
		this.$action 	= {};
		this.system_id = this.$minipanel.data('system-id');

		var that = this;
		this.$minipanel.find('.system-minipanel-bioinfo').each(function () {
			that.$bioinfo[$(this).data('bioinfo')] = $(this);
		});
		this.$minipanel.find('.system-minipanel-action').each(function () {
			$(this).on('click', function () {
				systemWebsocket.send_action(that.system_id, $(this).data('actor'), $(this).data('info'), Math.floor((new Date).getTime() / 1e3));
			});
			that.$action[$(this).data('action')] = $(this);
		});
		this.$minipanel.find('.system-minipanel-action-info').each(function () {
			$(this).on('input', function () {
				that.$action[$(this).data('to-action')].data('info', $(this).val());
			});
		});

		this.minichart = new SystemMinichart(id);
	}

	updateBioinfo (bio) {
		if (bio.waterlevel != null) this.$bioinfo.waterlevel.html(bio.waterlevel?ABOVE_TEXT:BELOW_TEXT);
		else this.$bioinfo.waterlevel.html('??');
		if (bio.brightness != null) this.$bioinfo.brightness.html(bio.brightness);
		else this.$bioinfo.brightness.html('??');
		if (bio.temperature != null) this.$bioinfo.temperature.html(bio.temperature);
		else this.$bioinfo.temperature.html('??');
		if (bio.humidity != null) this.$bioinfo.humidity.html(bio.humidity);
		else this.$bioinfo.humidity.html('??');
		if (bio.acidness != null) this.$bioinfo.acidness.html(bio.acidness);
		else this.$bioinfo.acidness.html('??');

		this.minichart.updateBioinfo(bio);
	}
}