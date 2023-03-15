<script lang="ts">
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	function arrowButton(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			console.log('arrow right');
		}

		if (event.key === 'ArrowLeft') {
			console.log('arrow left');
		}
	}
</script>

<svelte:window on:keydown={arrowButton} />

<ul>
	{#each data.chapter as { url, chapterTitle }}
		<li>
			<ImageLoader src={url} alt={chapterTitle} />
		</li>
	{/each}
</ul>
