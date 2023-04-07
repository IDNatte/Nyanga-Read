import { writable } from 'svelte/store';

export type ViewerPageType = {
	currentPage: number;
	totalPage: number;
};

export default writable<ViewerPageType>({ currentPage: 0, totalPage: 0 });
