import type { LayoutLoad } from './$types'
import { browser } from '$app/environment'

import { locale, waitLocale } from 'svelte-i18n'

import '../app.css'
import '$lib/i18n'

export const ssr = false
// export const prerender = true


export const load: LayoutLoad = async ({ fetch }) => {
  const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement

  // set Locale  
  if (browser) {
    locale.set(document.documentElement.lang)
  }

  const appInfo = async () => {
    const app = await fetch('http://localhost:5000/ipc/app', {
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
        'PCSRFWV-Token': pcsrfToken.value as string
      }
    })

    if (app.status === 200) {
      const appData = await app.json()
      return {
        appInfo: { about: appData.app_info.app_about }
      }
    } else {
      return {
        appInfo: null
      }
    }
  }

  const setting = async () => {
    const settings = await fetch('http://localhost:5000/ipc/settings', {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
        'PCSRFWV-Token': pcsrfToken.value as string
      }
    })

    if (settings.status === 200) {
      const settingsData = await settings.json()
      return { preferences: settingsData.settings }

    } else {
      return { preferences: null }
    }
  }

  await waitLocale()

  return {
    app: appInfo(),
    setting: setting()
  }

}
