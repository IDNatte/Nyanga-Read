import { writable } from 'svelte/store';

export type SearchEphemeralType = string | null;

export default writable<SearchEphemeralType>(null);
