import type { LayoutLoad } from './(pages)/$types';
import { browser } from '$app/environment';

import { locale, waitLocale } from 'svelte-i18n';
import '$lib/i18n';

export const prerender = true;

export const load: LayoutLoad = async () => {
	if (browser) {
		locale.set(document.documentElement.lang);
	}

	await waitLocale();
};
