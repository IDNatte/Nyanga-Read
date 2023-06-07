import dropdownStore from "$lib/store/dropdown/dropdown.store"

export default function outsideClick(node: HTMLElement) {
  const handleClick = (event: any) => {
    if (!node.contains(event.target)) {
      dropdownStore.set(false)
    }
  }

  document.addEventListener('click', handleClick, true)

  return {
    destroy() {
      document.removeEventListener('click', handleClick, true)
    }
  }
}