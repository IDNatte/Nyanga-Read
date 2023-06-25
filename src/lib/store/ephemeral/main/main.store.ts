import { writable } from "svelte/store";
import type { MainContentType } from "$lib/type/ephemeral/main";

export default writable<MainContentType>({ daily: [], bookmark: { bookmark_list: [], more: false } })