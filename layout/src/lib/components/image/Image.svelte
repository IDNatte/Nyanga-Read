<script lang="ts">
	import { onMount } from 'svelte';

	export let src: string;
	export let alt: string;

	let loaded: boolean = false;
	let thisImage: HTMLImageElement;

	onMount(() => {
		thisImage.onload = () => {
			loaded = true;
		};
	});
</script>

<img
	{src}
	{alt}
	class:loaded
	class="w-full h-auto rounded-t"
	bind:this={thisImage}
	loading="lazy"
/>

<style>
	img {
		opacity: 0;
		transition: opacity 1200ms ease-out;
	}
	img.loaded {
		opacity: 1;
	}
</style>
