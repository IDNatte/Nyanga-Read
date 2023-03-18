<script lang="ts">
	import { onMount } from 'svelte';

	import navigationStore from '$lib/store/navigation.store';
	import Image from '$lib/components/image/Image.svelte';
	import LazyloadComponent from '$lib/components/image/LazyloadComponent.svelte';

	export let src: string;
	export let alt: string;
	export let className: string = 'w-full h-auto rounded-t';

	let nativeLoading = false;

	onMount(() => {
		if ('loading' in HTMLImageElement.prototype) {
			nativeLoading = true;
			navigationStore.set('loading')
		}
	});
</script>

<LazyloadComponent {className} single={true} let:intersect={intersecting}>
	{#if intersecting || nativeLoading}
		<Image {className} {alt} {src} />
	{/if}
</LazyloadComponent>
