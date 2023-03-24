import type { LayoutLoad } from './$types';
import { browser } from '$app/environment';

import { locale, waitLocale } from 'svelte-i18n';
import '$lib/i18n';

export const ssr = false;
export const prerender = false;

export const load: LayoutLoad = async () => {
  if (browser) {
    if (window.navigator.language === 'en-US') {
      locale.set('en');
    } else {
      locale.set(window.navigator.language);
    }
  }

  await waitLocale();
};
