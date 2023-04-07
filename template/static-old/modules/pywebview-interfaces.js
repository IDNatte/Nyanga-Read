/* eslint-disable no-undef */
window.addEventListener('pywebviewready', () => {
	pywebview.api.ready().then((response) => {
		console.log(response);
	});

	document.addEventListener('send:frontend-version', (event) => {
		pywebview.api.getSvelteVersion(event.detail.version);
	});
});
