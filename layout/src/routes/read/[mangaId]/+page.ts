import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
  const getChapter = await fetch(`https://api.mangadex.org/manga/${params.mangaId}/aggregate`);

  const volumeContent = await getChapter.json();

  console.log(volumeContent)

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
      chapter
    });
  }

  return {
    volume,
    mangaId: params.mangaId
  };
};
