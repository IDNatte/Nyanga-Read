<script lang="ts">
	import Image from '$lib/components/image/Image.svelte';
	import LazyloadComponent from '$lib/components/image/LazyloadComponent.svelte';
	import { onMount } from 'svelte';

	export let src: string;
	export let alt: string;
	export let className: string = 'w-full h-auto rounded-t';

	let nativeLoading = false;

	onMount(() => {
		if ('loading' in HTMLImageElement.prototype) {
			nativeLoading = true;
		}
	});
</script>

<LazyloadComponent single={true} let:intersect={intersecting}>
	{#if intersecting || nativeLoading}
		<Image {className} {alt} {src} />
	{/if}
</LazyloadComponent>
