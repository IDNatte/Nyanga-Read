<script lang="ts">
	import ImageComponent from '$lib/components/image/ImageComponent.svelte';
	import LazyLoadComponent from '$lib/components/image/LazyLoadComponent.svelte';

	export let src: string | null | undefined;
	export let alt: string | null | undefined;
	export let className: string =
		'w-full h-full object-cover rounded-t transition-transform transform-gpu hover:scale-95';

	let nativeLoading = false;
</script>

<LazyLoadComponent {className} single={true} let:intersect={intersecting}>
	{#if intersecting || nativeLoading}
		<ImageComponent on:viewerimgloaded on:imageloaderror {className} {alt} {src} />
	{/if}
</LazyLoadComponent>
