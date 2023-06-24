import { writable } from "svelte/store";
import type { MainPageType } from "$lib/type/ephemeral/main";

export default writable<MainPageType>({ daily: [], bookmark: { bookmark_list: [], more: false } })