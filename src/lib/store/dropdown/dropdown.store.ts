import type { DropdownType } from "$lib/type/dropdown";
import { writable } from "svelte/store";

export default writable<DropdownType>(false);