import type { ImageViewerType } from '$lib/type/imgviewer';
import { writable } from 'svelte/store';

export default writable<ImageViewerType[]>([{ chapterNumber: null, url: null, index: null }]);
