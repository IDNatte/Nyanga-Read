<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	import ImageLoader from '$lib/components/image/ImageLoader.svelte';

	export let data: PageData;

	let imageSrc: string;
	let viewerWrapper: HTMLDivElement;

	function getArrayIndex(idxof: string): number {
		let index = data.chapter.findIndex(value => value.url == idxof)
		return index
	}

	function arrowButton(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			// next image
			viewerWrapper.scrollTop = 0
			let image = getArrayIndex(imageSrc)
			image += 1
			if (image >= data.chapter.length - 1) image = data.chapter.length - 1
			
			imageSrc = data.chapter[image].url

		}

		if (event.key === 'ArrowLeft') {
			// preview image
			viewerWrapper.scrollTop = 0
			let image = getArrayIndex(imageSrc)
			image -= 1
			if (image <= 0) image = 0

			imageSrc = data.chapter[image].url

		}
	}

	onMount(() => {
		imageSrc = data.chapter[0].url
	})
</script>

<svelte:window on:keydown={arrowButton} />

<div class="flex justify-center items-center" bind:this={viewerWrapper}>
	<ImageLoader src={imageSrc} alt={"testing"} className="rounded-none flex justify-center"/>
</div>
