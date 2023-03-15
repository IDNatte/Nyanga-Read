import { writable } from 'svelte/store';
import type { AccordionType } from '$lib/ui/accordion.store.type';

export default writable<AccordionType>({ accordionId: null, accordionOpen: null });
