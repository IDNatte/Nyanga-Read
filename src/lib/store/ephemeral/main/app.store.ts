import { writable } from "svelte/store";
import type { AppInfoType } from "$lib/type/ephemeral/main";

export default writable<AppInfoType>({ info: null })