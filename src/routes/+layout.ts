import '../app.css'
import { error } from '@sveltejs/kit';
import type { LayoutLoad } from './$types'

import csrfStore from '$lib/store/csrf/csrf.store';

export const ssr = false
export const prerender = true

export const load: LayoutLoad = async ({ fetch }) => {
  const fetchToken = await fetch('http://127.0.0.1:5000/init')

  if (fetchToken.status !== 200) {
    const init = await fetchToken.json()
    throw error(init.code, init.detail)
  }

  if (fetchToken.status === 200) {
    const init = await fetchToken.json()
    csrfStore.set(init.csrf_token)
  }
}