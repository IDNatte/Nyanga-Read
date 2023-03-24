import { browser } from '$app/environment';
import { init, register } from 'svelte-i18n';

const defaultLocale = 'id';

register('en', () => import('./locales/en.json'));
register('id', () => import('./locales/id.json'));

function initLocale() {
	if (browser) {
		if (window.navigator.language === 'en-US') {
			return 'en';
		} else {
			return window.navigator.language;
		}
	}
}

init({
	fallbackLocale: defaultLocale,
	initialLocale: initLocale()
});
