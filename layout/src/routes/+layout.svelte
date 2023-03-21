<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import toast, { Toaster } from 'svelte-french-toast';
	import navigationStore from '$lib/store/navigation.store';
	import PageLoaderComponent from '$lib/components/loader/PageLoaderComponent.svelte';
	import '../app.css';
	import mangaStore from '$lib/store/manga.store';

	onMount(() => {
		document.addEventListener('manga-action:info', (event: any) => {
			toast(event.detail.info, { icon: '😸', position: 'top-right' });
		});

		document.addEventListener('manga-action:load', (event: any) => {
			mangaStore.set(event.detail.data);
		});
	});
</script>

{#if $navigationStore === 'loading'}
	<div out:fade={{ delay: 500 }}>
		<PageLoaderComponent />
	</div>
{/if}

<main>
	<slot />
</main>

<Toaster />
