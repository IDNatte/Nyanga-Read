import type { DropdownType } from "$lib/type/ui/dropdown";
import { writable } from "svelte/store";

export default writable<DropdownType>({ dropdown: null, open: false });