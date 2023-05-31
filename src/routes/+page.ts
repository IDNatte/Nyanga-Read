import type { PageLoad } from "./$types";
import csrfStore from "$lib/store/csrf/csrf.store";
import { get } from "svelte/store";

export const load: PageLoad = async ({ fetch }) => {
  const daily = await fetch('http://localhost:5000/ipc/init', {
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
      'PCSRFWV-Token': get(csrfStore) as string
    }
  })

  const dailyContent = await daily.json()

  return {
    daily: dailyContent.daily_data.data
  }
}