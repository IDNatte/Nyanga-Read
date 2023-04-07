import { writable } from 'svelte/store';

export type ModalDropdwonType = {
	modal: string | null;
	open?: boolean;
};

export default writable<ModalDropdwonType>({ modal: null, open: false });
