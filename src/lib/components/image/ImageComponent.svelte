<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import loaderStore from '$lib/store/loader/loader.store';

	export let src: string;
	export let alt: string;
	export let className: string;

	const dispatch: any = createEventDispatcher();
	let loaded: boolean = false;
	let thisImage: HTMLImageElement;

	onMount(() => {
		thisImage.onload = () => {
			dispatch('viewerimgloaded', {
				image: src
			});

			loaded = true;
			loaderStore.set('loaded');
		};

		thisImage.onerror = () => {
			dispatch('imageloaderror');
			loaded = false;
			loaderStore.set('loaded');
		};
	});
</script>

<img {src} {alt} class:loaded class={className} bind:this={thisImage} loading="lazy" />

<style>
	img {
		opacity: 0;
		transition: opacity 1200ms ease-out;
	}
	img.loaded {
		opacity: 1;
	}
</style>
