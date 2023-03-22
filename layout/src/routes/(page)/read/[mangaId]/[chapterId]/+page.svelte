<script lang="ts">
	import type { PageData } from './$types';
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import viewerStore from '$lib/store/viewer.store';

	export let data: PageData;

	$viewerStore.totalPage = data.chapter.length;

	let imageSrc: string;
	let imageAlt: string;
	let navigation: string;

	function getArrayIndex(idxof: string): number {
		let index = data.chapter.findIndex((value) => value.url == idxof);
		return index;
	}

	function arrowButton(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			// next image
			let image = getArrayIndex(imageSrc);
			// let page = $viewerStore.currentPage + 1;
			navigation = 'next'
			image += 1;

			if (image >= data.chapter.length - 1) {
				image = data.chapter.length - 1;
				// page = data.chapter.length ;
			}

			// $viewerStore.currentPage = page;

			imageSrc = data.chapter[image].url;
			imageAlt = data.chapter[image].chapterTitle;
		}

		if (event.key === 'ArrowLeft') {
			// preview image
			let image = getArrayIndex(imageSrc);
			// let page = $viewerStore.currentPage - 1;
			navigation = 'prev'

			image -= 1;
			if (image <= 0) {
				image = 0;
				// page = 1;
			}

			// $viewerStore.currentPage = page;

			imageSrc = data.chapter[image].url;
			imageAlt = data.chapter[image].chapterTitle;
		}
	}

	function viewerImageLoad() {
		let currentPage = $viewerStore.currentPage
		if (navigation === 'prev') {
			if ($viewerStore.currentPage === 1) {
				$viewerStore.currentPage = 1
			} else {
				$viewerStore.currentPage = currentPage - 1
			}
		} else if (navigation === 'next') {
			if ($viewerStore.currentPage === $viewerStore.totalPage) {
				$viewerStore.currentPage = $viewerStore.totalPage + 1
			} else {
				$viewerStore.currentPage = currentPage + 1
			}
		}
	}

	document.addEventListener('viewer-change:next', () => {
		let image = getArrayIndex(imageSrc);
		let page = $viewerStore.currentPage + 1;
		image += 1;
		if (image >= data.chapter.length - 1) {
			image = data.chapter.length - 1;
			page = data.chapter.length;
		}

		$viewerStore.currentPage = page;

		imageSrc = data.chapter[image].url;
		imageAlt = data.chapter[image].chapterTitle;
	});

	document.addEventListener('viewer-change:prev', () => {
		let image = getArrayIndex(imageSrc);
		let page = $viewerStore.currentPage - 1;

		image -= 1;
		if (image <= 0) {
			image = 0;
			page = 1;
		}

		$viewerStore.currentPage = page;

		imageSrc = data.chapter[image].url;
		imageAlt = data.chapter[image].chapterTitle;
	});

	onMount(() => {
		imageSrc = data.chapter[0].url;
		imageAlt = data.chapter[0].chapterTitle;
		$viewerStore.currentPage = 1;
	});

	onDestroy(() =>{
		viewerStore.set({currentPage: 1, totalPage: 0})
	})
</script>

<svelte:window on:keydown={arrowButton} />

<div class="flex justify-center items-center" in:fade={{ duration: 200 }}>
	<ImageLoader
		src={imageSrc}
		alt={`Chapter ${imageAlt}`}
		className="rounded-none flex justify-center"
		on:imgloaded={viewerImageLoad}
	/>
</div>
