import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const getChapter = await fetch(
		`https://api.mangadex.org/manga/${params.mangaId}/aggregate?translatedLanguage[]=${document.documentElement.lang}`
	);

	const getManga = await fetch(
		`https://api.mangadex.org/manga/${params.mangaId}?includes[]=cover_art`
	);

	const volumeContent = await getChapter.json();
	const manga = await getManga.json();

	const coverArt = manga.data.relationships;
	const title = manga.data.attributes.title.en || manga.data.attributes.title.ja;
	const description = manga.data.attributes.description.en || manga.data.attributes.description.ja;
	const volume = [];

	for (const data in volumeContent.volumes) {
		const chapter = [];

		for (const chapterData in volumeContent.volumes[data].chapters) {
			chapter.push({
				chapterName: volumeContent.volumes[data].chapters[chapterData].chapter,
				chapterId: volumeContent.volumes[data].chapters[chapterData].id
			});
		}

		volume.push({
			volume: data,
			chapter: chapter.sort((a, b) => Number(b.chapterName) - Number(a.chapterName))
		});
	}

	return {
		volume: volume.sort((a, b) => Number(b.volume) - Number(a.volume)),
		mangaId: params.mangaId,
		cover: coverArt,
		title,
		description
	};
};
