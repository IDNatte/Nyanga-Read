import { writable } from 'svelte/store';

export type LanguageMenuDropdwonType = boolean;

export default writable<LanguageMenuDropdwonType>(false);
