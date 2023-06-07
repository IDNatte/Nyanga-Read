export default function refresh(node: HTMLElement, params: any) {
  const shortcut = (event: any) => {
    if ((!!params.alt != event.altKey) ||
      (!!params.shift != event.shiftKey) ||
      (!!params.control != (event.ctrlKey || event.metaKey)) ||
      params.code != event.code) {
      return;
    }

    event.preventDefault()
    params.callback ? params.callback() : node.click()

  }

  document.addEventListener('keydown', shortcut)
  return {
    destroy() {
      document.removeEventListener('keydown', shortcut)
    }
  }
}