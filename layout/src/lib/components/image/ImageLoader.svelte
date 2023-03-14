<script lang="ts">
	import Image from '$lib/components/image/Image.svelte';
	import LazyloadComponent from '$lib/components/image/LazyloadComponent.svelte';
	import { onMount } from 'svelte';

	export let src: string;
	export let alt: string;

	let nativeLoading = false;

	onMount(() => {
		if ('loading' in HTMLImageElement.prototype) {
			nativeLoading = true;
		}
	});
</script>

<LazyloadComponent single={true} let:intersect={intersecting}>
	{#if intersecting || nativeLoading}
		<Image {alt} {src} />
	{/if}
</LazyloadComponent>
