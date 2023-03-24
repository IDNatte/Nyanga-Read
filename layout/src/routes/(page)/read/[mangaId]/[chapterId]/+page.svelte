<script lang="ts">
	import type { PageData } from './$types';
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import viewerStore from '$lib/store/viewer.store';

	import toast, { Toaster } from 'svelte-french-toast';
	import ViewerToastComponent from '$lib/components/toast/ViewerToastComponent.svelte';

	export let data: PageData;

	$viewerStore.totalPage = data.chapter.length;

	let imageSrc: string;
	let imageAlt: string;

	function getArrayIndex(idxof: string): number {
		let index = data.chapter.findIndex((value) => value.url == idxof);
		return index;
	}

	function arrowButton(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			// next image
			let image = getArrayIndex(imageSrc);
			image += 1;

			if (image >= data.chapter.length - 1) image = data.chapter.length - 1;

			imageSrc = data.chapter[image].url;
			imageAlt = data.chapter[image].chapterTitle;
		}

		if (event.key === 'ArrowLeft') {
			// preview image
			let image = getArrayIndex(imageSrc);

			image -= 1;
			if (image <= 0) image = 0;

			imageSrc = data.chapter[image].url;
			imageAlt = data.chapter[image].chapterTitle;
		}
	}

	function viewerImageLoad(event: any) {
		$viewerStore.currentPage = event.detail.image.split('/')[5].split('-')[0];
		window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
	}

	function viewerImageError() {
		toast.error(ViewerToastComponent, { position: 'bottom-left', duration: 1500 });
	}

	document.addEventListener('viewer-change:next', () => {
		let image = getArrayIndex(imageSrc);
		image += 1;

		if (image >= data.chapter.length - 1) image = data.chapter.length - 1;

		imageSrc = data.chapter[image].url;
		imageAlt = data.chapter[image].chapterTitle;
	});

	document.addEventListener('viewer-change:prev', () => {
		let image = getArrayIndex(imageSrc);
		image -= 1;
		if (image <= 0) image = 0;

		imageSrc = data.chapter[image].url;
		imageAlt = data.chapter[image].chapterTitle;
	});

	onMount(() => {
		imageSrc = data.chapter[0].url;
		imageAlt = data.chapter[0].chapterTitle;
		$viewerStore.currentPage = 1;
	});

	onDestroy(() => {
		viewerStore.set({ currentPage: 1, totalPage: 0 });
	});
</script>

<svelte:window on:keydown={arrowButton} />

<div class="flex justify-center items-center pt-[2.2rem] px-6 pb-28" in:fade={{ duration: 200 }}>
	<ImageLoader
		src={imageSrc}
		alt={`Chapter ${imageAlt}`}
		className="rounded-none flex justify-center"
		on:viewerimgloaded={viewerImageLoad}
		on:imageloaderror={viewerImageError}
	/>
</div>

<Toaster />
