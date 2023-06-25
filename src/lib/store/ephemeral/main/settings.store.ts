import { writable } from "svelte/store";
import type { AppSettingType } from "$lib/type/ephemeral/main";

export default writable<AppSettingType>({ settings: null })