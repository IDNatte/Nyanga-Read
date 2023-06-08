import type { PageLoad } from "./$types";


export const load: PageLoad = async ({ fetch, params }) => {
  const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement

  const manga = await fetch(`http://localhost:5000/ipc/get_detail/${params.manga}`, {
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
      'PCSRFWV-Token': pcsrfToken.value as string
    }
  })

  const detailData = await manga.json()



  return {
    manga: detailData.detail_data.data
  }
}