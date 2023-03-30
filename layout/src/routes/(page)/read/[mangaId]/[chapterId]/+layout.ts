import type { LayoutLoad } from './$types';

export const load: LayoutLoad = ({ url }) => {
	return {
		chapterName: url.searchParams.get('chapterName'),
		volumeName: url.searchParams.get('volumeName'),
		manga: url.searchParams.get('manga'),
		chapter: url.searchParams.get('chapter')
	};
};
