import type { LayoutLoad } from './$types';
import { browser } from '$app/environment';

import { locale, waitLocale } from 'svelte-i18n';
import '$lib/i18n';

export const ssr = false;
export const prerender = false;

export const load: LayoutLoad = async () => {
	if (browser) {
		locale.set(document.documentElement.lang);
	}

	await waitLocale();
};
