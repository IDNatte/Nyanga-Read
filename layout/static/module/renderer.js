document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('manga-action:saveLocal', (event) => {
		window.backendAPI.triggerSave(event.detail.mangaId);
	});

	document.addEventListener('request:manga-load', () => {
		window.backendAPI.triggerMangaLoad();
	});

	document.addEventListener('request:manga-load-all', () => {
		window.backendAPI.triggerMangaLoadAll();
	});

	document.addEventListener('request:app-about', () => {
		window.backendAPI.triggerAppAbout();
	});

	document.addEventListener('request:app-update', () => {
		window.backendAPI.triggerAppUpdate();
	});

	document.addEventListener('request:app-instal-update', () => {
		window.backendAPI.triggerAppApplyUpdate();
	});

	window.backendAPI.onMangaSave((e, data) => {
		let mangaAction = new CustomEvent('manga-action:info', { detail: { info: data } });
		document.dispatchEvent(mangaAction);
	});

	window.backendAPI.onMangaLoad((e, data) => {
		let mangaLoad = new CustomEvent('manga-action:load', { detail: { data } });
		document.dispatchEvent(mangaLoad);
	});

	window.backendAPI.onMangaLoadAll((e, data) => {
		let mangaLoadAll = new CustomEvent('manga-action:load-all', { detail: { data } });
		document.dispatchEvent(mangaLoadAll);
	});

	window.backendAPI.onAppAbout((e, data) => {
		let appAbout = new CustomEvent('app-action:about', { detail: { data } });
		document.dispatchEvent(appAbout);
	});

	window.backendAPI.onAppUpdate((e, data) => {
		let appUpdate = new CustomEvent('app-action:update', { detail: { data } });
		document.dispatchEvent(appUpdate);
	});
});
