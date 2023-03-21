import { writable } from 'svelte/store';

type MangaListArrayType = [
	{
		mangaId: string;
	}
];

type MangaListType = {
	manga: MangaListArrayType,
	page?: boolean
}

export type MangaStoreType = MangaListType;

export default writable<MangaStoreType>({ manga: [{ mangaId: '' }], page: false });
