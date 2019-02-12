function parseQueryString (data) {
	return Object.keys(data).map(
		k => encodeURIComponent(k) + '=' + encodeURIComponent(data[k])).join('&');
}