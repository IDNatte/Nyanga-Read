import type { DailyListsEphemeralType } from "$lib/type/ephemeral/dailylists";
import { writable } from "svelte/store";

export default writable<DailyListsEphemeralType>({ data: [], page: 1, scroll: 0 })