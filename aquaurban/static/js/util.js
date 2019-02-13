function parseQueryString (data) {
	return Object.keys(data).map(
		k => encodeURIComponent(k) + '=' + encodeURIComponent(data[k])).join('&');
}

function dateToUnixSeconds (date) {
	return Math.round(date.getTime() / 1e3);
}

moment.locale(navigator.language);