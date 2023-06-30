import type { LoaderType } from "$lib/type/loader";
import { writable } from "svelte/store";

export default writable<LoaderType>(null);