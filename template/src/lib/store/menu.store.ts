import { writable } from 'svelte/store';

export type MenuDropdwonType = boolean;

export default writable<MenuDropdwonType>(false);
