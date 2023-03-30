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

	document.addEventListener('request:win-minimize', () => {
		window.backendAPI.triggreWinMinimize();
	});

	document.addEventListener('request:win-resize', () => {
		window.backendAPI.triggerWinResize();
	});

	document.addEventListener('request:win-close', () => {
		window.backendAPI.triggreWinClose();
	});

	document.addEventListener('request:app-get-lang', () => {
		window.backendAPI.triggerAppGetLanguage();
	});

	document.addEventListener('request:app-set-lang', (event) => {
		window.backendAPI.triggerAppSetLanguage(event.detail);
	});

	document.addEventListener('request:check-app', () => {
		window.backendAPI.triggerAppCheckInit();
	});

	document.addEventListener('request:app-full-reload', () => {
		window.backendAPI.triggerAppFullReload();
	});

	document.addEventListener('request:set-last-read', (event) => {
		let data = {
			manga: event.detail.manga,
			chapter: event.detail.chapter,
			volumeName: event.detail.volumeName,
			chapterName: event.detail.chapterName
		};
		window.backendAPI.triggerMangaSetLastRead(data);
	});

	document.addEventListener('request:get-last-read', (event) => {
		window.backendAPI.triggerMangaGetLastRead(event.detail.manga);
	});

	window.backendAPI.onAppCheckInit((e, data) => {
		const appInitRun = new CustomEvent('app-action:init', { detail: data });
		document.dispatchEvent(appInitRun);
	});

	window.backendAPI.onGetAppLang((e, data) => {
		const appLanguage = new CustomEvent('app-action:language', { detail: { data } });
		document.dispatchEvent(appLanguage);
	});

	window.backendAPI.onMangaGetLastRead((e, data) => {
		const mangaAction = new CustomEvent('manga-action:last-read', { detail: data });
		document.dispatchEvent(mangaAction);
	});

	window.backendAPI.onMangaSave((e, data) => {
		const mangaAction = new CustomEvent('manga-action:info', { detail: { info: data } });
		document.dispatchEvent(mangaAction);
	});

	window.backendAPI.onMangaLoad((e, data) => {
		const mangaLoad = new CustomEvent('manga-action:load', { detail: { data } });
		document.dispatchEvent(mangaLoad);
	});

	window.backendAPI.onMangaLoadAll((e, data) => {
		const mangaLoadAll = new CustomEvent('manga-action:load-all', { detail: { data } });
		document.dispatchEvent(mangaLoadAll);
	});

	window.backendAPI.onAppAbout((e, data) => {
		const appAbout = new CustomEvent('app-action:about', { detail: { data } });
		document.dispatchEvent(appAbout);
	});

	window.backendAPI.onAppUpdate((e, data) => {
		const appUpdate = new CustomEvent('app-action:update', { detail: { data } });
		document.dispatchEvent(appUpdate);
	});

	window.backendAPI.onAppError((e, data) => {
		const appError = new CustomEvent('app-action:error', { detail: data });
		console.log(data);
		document.dispatchEvent(appError);
	});
});
