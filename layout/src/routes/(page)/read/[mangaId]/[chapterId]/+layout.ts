import type { LayoutLoad } from './$types';

export const load: LayoutLoad = ({ url }) => {
	return {
		volume: url.searchParams.get('volume'),
		chapter: url.searchParams.get('chapter')
	};
};
