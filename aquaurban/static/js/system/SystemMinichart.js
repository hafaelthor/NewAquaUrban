DEFAULT_CHART_OPTIONS = {
	scales: {
		yAxes: [
		{ticks: {beginAtZero:true}}]
	}
};

DEFAULT_CHART_TYPE = 'line';

CHART_WATERLEVEL_INDEX = 0;
CHART_BRIGHTNESS_INDEX = 1;
CHART_TEMPERATURE_INDEX = 2;
CHART_HUMIDITY_INDEX = 3;
CHART_ACIDNESS_INDEX = 4;

DATETIME_REGEX = /(?<month>\d+)-(?<day>\d{2})-(?<year>\d{2})T(?<hour>\d{2}):(?<minute>\d{2})/

class SystemMinichart {
	constructor (id) {
		this.keep_updating 	= true; 
		this.$canvas 		= $('.system-minichart[data-id="' + id + '"]');
		this.system_id 		= this.$canvas.data('system-id');
		this.$form 			= $('.system-minichart-query[data-id="' + id + '"]');
		this.chart = new Chart(this.$canvas, {
			type: DEFAULT_CHART_TYPE,
			data: {
				datasets: [
					{
						label: WATERLEVEL_TEXT,
						backgroundColor: 'rgba(0, 0, 0, 0)',
						borderColor: 'rgba(255,99,0,1)',
						borderWidth: 1
					},
					{
						label: BRIGHTNESS_TEXT,
						backgroundColor: 'rgba(0, 0, 0, 0)',
						borderColor: 'rgba(255,199,13,1)',
						borderWidth: 1
					},
					{
						label: TEMPERATURE_TEXT,
						backgroundColor: 'rgba(0, 0, 0, 0)',
						borderColor: 'rgba(100,199,13,1)',
						borderWidth: 1
					},
					{
						label: HUMIDITY_TEXT,
						backgroundColor: 'rgba(0, 0, 0, 0)',
						borderColor: 'rgba(255,0,255,1)',
						borderWidth: 1
					},
					{
						label: ACIDNESS_TEXT,
						backgroundColor: 'rgba(0, 0, 0, 0)',
						borderColor: 'rgba(100,199,130,1)',
						borderWidth: 1
					}
				]
			},
			options: DEFAULT_CHART_OPTIONS
		});
		this.updateAll(this.queryBioLast());
		var that = this;
		this.$form.submit(function (event) {
			switch ($(this).find('input[type=submit]:focus').attr('name')) {
				case 'recent':
					that.updateAll(that.queryBioLast());
					that.keep_updating = true;
					break;
				case 'query':
					let ti = new Date(event.target[1].value);
					let tf = new Date(event.target[2].value);
					that.updateAll(that.queryBioInterval(ti, tf));
					that.keep_updating = false;
			}
			event.preventDefault();
		});
	}

	updateLast (bio) {
		this.chart.data.labels.push(parseChartTimestamp(bio.timestamp));
		this.chart.data.datasets[CHART_WATERLEVEL_INDEX].data.push(parseChartWaterlevel(bio.waterlevel));
		this.chart.data.datasets[CHART_BRIGHTNESS_INDEX].data.push(parseChartBrightness(bio.brightness));
		this.chart.data.datasets[CHART_TEMPERATURE_INDEX].data.push(parseChartTemperature(bio.temperature));
		this.chart.data.datasets[CHART_HUMIDITY_INDEX].data.push(parseChartHumidity(bio.humidity));
		this.chart.data.datasets[CHART_ACIDNESS_INDEX].data.push(parseChartAcidness(bio.acidness));
		this.chart.update();
	}

	updateBioinfo (bio) {
		if (!this.keep_updating) return;
		this.updateLast(bio);
		this.dropFirst();
	}

	dropFirst () {
		this.chart.data.labels.shift();
		this.chart.data.datasets[CHART_WATERLEVEL_INDEX].data.shift();
		this.chart.data.datasets[CHART_BRIGHTNESS_INDEX].data.shift();
		this.chart.data.datasets[CHART_TEMPERATURE_INDEX].data.shift();
		this.chart.data.datasets[CHART_HUMIDITY_INDEX].data.shift();
		this.chart.data.datasets[CHART_ACIDNESS_INDEX].data.shift();
		this.chart.update();
	}

	updateAll (bio_set) {
		this.chart.data.labels = bio_set.timestamp.map(parseChartTimestamp);
		this.chart.data.datasets[CHART_WATERLEVEL_INDEX].data = bio_set.waterlevel.map(parseChartWaterlevel);
		this.chart.data.datasets[CHART_BRIGHTNESS_INDEX].data = bio_set.brightness.map(parseChartBrightness);
		this.chart.data.datasets[CHART_TEMPERATURE_INDEX].data = bio_set.temperature.map(parseChartTemperature);
		this.chart.data.datasets[CHART_HUMIDITY_INDEX].data = bio_set.humidity.map(parseChartHumidity);
		this.chart.data.datasets[CHART_ACIDNESS_INDEX].data = bio_set.acidness.map(parseChartAcidness);
		this.chart.update();
	}

	queryBioInterval (ti, tf) {
		return $.ajax({
			url: `hquery/${this.system_id}?${parseQueryString({ti: Math.round(ti.getTime() / 1e3), tf: Math.round(tf.getTime() / 1e3)})}`,
			async: false
		}).responseJSON;
	}

	queryBioLast () {
		return $.ajax({
			url: `hlast/${this.system_id}`,
			async: false
		}).responseJSON;
	}
}

function parseChartTimestamp (timestamp) {
	if (timestamp == null) return null;
	let date = new Date(timestamp * 1e3); 
	return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
}

function parseChartWaterlevel (waterlevel) {
	if (waterlevel == null) return null;
	return 10 * +waterlevel;
}

function parseChartBrightness (brightness) {
	if (brightness == null) return null;
	return brightness / 1e5;
}

function parseChartTemperature (temperature) {
	if (temperature == null) return null;
	return temperature;
}

function parseChartHumidity (humidity) {
	if (humidity == null) return null;
	return humidity;
}

function parseChartAcidness (acidness) {
	if (acidness == null) return null;
	return acidness;
}