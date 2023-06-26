import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
  const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement

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