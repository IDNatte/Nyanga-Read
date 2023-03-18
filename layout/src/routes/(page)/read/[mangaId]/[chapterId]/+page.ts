import type { PageLoad } from './$types';
import navigationStore from '$lib/store/navigation.store';

export const load: PageLoad = async ({ fetch, params }) => {
	const getChapterMeta = async () => {
		const chapterMeta = await fetch(`https://api.mangadex.org/at-home/server/${params.chapterId}`);
		const chapter = await chapterMeta.json();

		navigationStore.set('loaded')

		const chapterData = [];

		for (const chapterImg in chapter.chapter.data) {
			chapterData.push({
				url: `${chapter.baseUrl}/data/${chapter.chapter.hash}/${chapter.chapter.data[chapterImg]}`,
				chapterTitle: `${chapter.chapter.data[chapterImg].split('-')[0]}`
			});
		}

		return chapterData;
	};

	return {
		chapter: getChapterMeta(),
		chapterId: params.chapterId
	};
};
