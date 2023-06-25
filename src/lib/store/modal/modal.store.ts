import { writable } from 'svelte/store';
import type { ModalType } from '$lib/type/ui/modal';


export default writable<ModalType>({ modal: null, open: false });
