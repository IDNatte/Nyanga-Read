<script lang="ts">
	import { onMount } from 'svelte';

	import loaderStore from '$lib/store/loader/loader.store';
	import ImageComponent from '$lib/components/image/ImageComponent.svelte';
	import LazyLoadComponent from '$lib/components/image/LazyLoadComponent.svelte';

	export let src: string;
	export let alt: string;
	export let className: string =
		'w-full h-full object-cover rounded-t transition-transform transform-gpu hover:scale-95';

	let nativeLoading = false;

	onMount(() => {
		if ('loading' in HTMLImageElement.prototype) {
			loaderStore.set('loading');
		}
	});
</script>

<LazyLoadComponent {className} single={true} let:intersect={intersecting}>
	{#if intersecting || nativeLoading}
		<ImageComponent on:viewerimgloaded on:imageloaderror {className} {alt} {src} />
	{/if}
</LazyLoadComponent>
