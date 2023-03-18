<script>
	import { fade } from 'svelte/transition';
	// import { afterNavigate, beforeNavigate } from '$app/navigation';

	import navigationStore from '$lib/store/navigation.store';
	import PageLoaderComponent from '$lib/components/loader/PageLoaderComponent.svelte';
	import '../app.css';
</script>

{#if $navigationStore === 'loading'}
	<div out:fade={{ delay: 500 }}>
		<PageLoaderComponent />
	</div>
{/if}

<main>
	<slot />
</main>
