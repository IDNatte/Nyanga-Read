import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
  const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement

  const content = async () => {
    const content = await fetch('http://localhost:5000/ipc/init', {
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
        'PCSRFWV-Token': pcsrfToken.value as string
      }
    })

    // const 

    if (content.status === 200) {
      const contentData = await content.json()
      return {
        daily: contentData.daily_manga.data,
        bookmark: {
          bookmark_list: contentData.bookmark.bookmark_manga,
          more: contentData.bookmark.more
        }
      }
    } else {
      return {
        daily: [],
        bookmark: {
          bookmark_list: [],
          more: false
        }
      }
    }
  }

  const appInfo = async () => {
    const app = await fetch('http://localhost:5000/ipc/app', {
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
        'PCSRFWV-Token': pcsrfToken.value as string
      }
    })

    // const 

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
      return { settings: settingsData }
    } else {
      return { settings: null }

    }
  }

  return {
    content: content(),
    setting: setting(),
    appInfo: appInfo()
  }
}