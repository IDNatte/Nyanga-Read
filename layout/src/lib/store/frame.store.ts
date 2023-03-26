import { writable } from 'svelte/store';

export type FrameTitleType = string;

export default writable<FrameTitleType>('read nyanga');
