document.addEventListener('DOMContentLoaded', () => {
	console.log('Renderer ready...!!!');

	document.addEventListener('manga-action:saveLocal', (event) => {
		window.backendAPI.triggerSave(event.detail.mangaId);
	});

	document.addEventListener('request:manga-load', () => {
		window.backendAPI.triggerMangaLoad();
	});

	document.addEventListener('request:manga-load-all', () => {
		window.backendAPI.triggerMangaLoadAll()
	})

	window.backendAPI.onMangaSave((e, data) => {
		let mangaAction = new CustomEvent('manga-action:info', { detail: { info: data } });
		document.dispatchEvent(mangaAction);
	});

	window.backendAPI.onMangaLoad((e, data) => {
		let mangaLoad = new CustomEvent('manga-action:load', { detail: { data } });
		document.dispatchEvent(mangaLoad);
	});

	window.backendAPI.onMangaLoadAll((e, data) => {
		let mangaLoadAll = new CustomEvent('manga-action:load-all', {detail: {data}})
		document.dispatchEvent(mangaLoadAll)
	})
});
