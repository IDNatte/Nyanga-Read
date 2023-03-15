import type { PageLoad } from './$types'

export const load: PageLoad = ({ params }) => {
  const which = params.which
  return {
    which
  }
}