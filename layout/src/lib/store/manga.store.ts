import { writable } from 'svelte/store';

type MangaListType = [{
  mangaId: string,
  meta?: any
}]

export type MangaStoreType = MangaListType;

export default writable<MangaStoreType>([{ mangaId: '' }]);
