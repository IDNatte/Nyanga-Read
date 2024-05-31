import type { DetailEphemeralType } from '$lib/type/ephemeral/detail';
import { writable } from 'svelte/store';

export default writable<DetailEphemeralType>({
	page: 1,
	bookmarked: false,
	detail_data: null,
	last_read: null,
	manga_data: [],
	paginated: false
});
