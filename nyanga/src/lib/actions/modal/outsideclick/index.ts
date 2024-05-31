import modalStore from '$lib/store/modal/modal.store';

export default function outsideClick(node: HTMLElement) {
	const handleClick = (event: any) => {
		if (!node.contains(event.target)) {
			modalStore.set({ modal: null, open: false });
		}
	};

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	};
}
