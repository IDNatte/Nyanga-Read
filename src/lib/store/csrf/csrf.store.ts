import type { CSRFTokenType } from "$lib/type/csrf";
import { writable } from "svelte/store";

export default writable<CSRFTokenType>(null);