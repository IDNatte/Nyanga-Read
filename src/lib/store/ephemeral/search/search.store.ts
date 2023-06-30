import { writable } from "svelte/store";
import type { SearchEphemeralType } from "$lib/type/ephemeral/search";

export default writable<SearchEphemeralType>(null)