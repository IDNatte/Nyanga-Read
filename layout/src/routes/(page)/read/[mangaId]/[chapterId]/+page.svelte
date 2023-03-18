<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	import ImageLoader from '$lib/components/image/ImageLoader.svelte';

	export let data: PageData;

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
	});
</script>

<svelte:window on:keydown={arrowButton} />

<div class="flex justify-center items-center">
	<ImageLoader
		src={imageSrc}
		alt={`Chapter ${imageAlt}`}
		className="rounded-none flex justify-center"
	/>
</div>
