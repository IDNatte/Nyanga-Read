<script lang="ts">
	import loaderStore from '$lib/store/loader/loader.store';
	import { createEventDispatcher, onMount } from 'svelte';

	export let alt: string | null | undefined;
	export let src: string | null | undefined;
	export let className: string;

	const dispatch: any = createEventDispatcher();
	let loaded: boolean = false;
	let thisImage: HTMLImageElement;
	let error: boolean = false;

	loaderStore.set('loading');
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
			error = true;
		};
	});
</script>

{#if !loaded}
	<div class="animate-pulse bg-slate-200 w-full min-h-[580px] rounded"></div>
{/if}

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
