import mainStore from "$lib/store/ephemeral/main/main.store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
  const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement

  const daily = await fetch('http://localhost:5000/ipc/init', {
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
      'PCSRFWV-Token': pcsrfToken.value as string
    }
  })

  if (daily.status === 200) {
    const dailyContent = await daily.json()
    mainStore.set({ daily: dailyContent.daily_data.data, bookmark: [] })
    // mainStore.set({ daily: [], bookmark: [] })

  } else {
    mainStore.set({ daily: [], bookmark: [] })
  }

}