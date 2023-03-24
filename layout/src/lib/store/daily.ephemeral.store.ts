import { writable } from 'svelte/store';

export type DailyEphemeralType = {
	offset: number;
	limit: number;
	data: Array<any>;
	scrollPos: number;
};

export default writable<DailyEphemeralType>({ offset: 0, limit: 0, data: [], scrollPos: 0 });
