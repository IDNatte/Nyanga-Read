<script lang="ts">
	import { fade } from 'svelte/transition';

	import toast, {Toaster} from 'svelte-french-toast';
	import navigationStore from '$lib/store/navigation.store';
	import PageLoaderComponent from '$lib/components/loader/PageLoaderComponent.svelte';
	import '../app.css';
	import { onMount } from 'svelte';

	onMount(() => {
		document.addEventListener('manga-action:info', (event:any) => {
			toast(event.detail.info, {icon: '😸', position: 'top-right'})
		})
	})
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
