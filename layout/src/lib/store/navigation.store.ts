import { writable } from 'svelte/store';

export type NavigationStore = 'loading' | 'loaded' | null;

export default writable<NavigationStore>(null);
