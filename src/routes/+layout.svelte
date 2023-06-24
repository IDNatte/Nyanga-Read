<script lang="ts">
	import { onMount } from 'svelte';
	import { invalidateAll } from '$app/navigation';
	import { fade } from 'svelte/transition';

	import { Toaster } from 'svelte-french-toast';

	import refresh from '$lib/actions/page/refresh';
	import csrfStore from '$lib/store/csrf/csrf.store';
	import loaderStore from '$lib/store/loader/loader.store';

	import PageLoader from '$lib/components/loader/PageLoader.svelte';

	onMount(() => {
		let pycsrf = document.querySelector('.pycsrf') as HTMLInputElement;
		csrfStore.set(pycsrf.value);
	});
</script>

{#if $loaderStore === 'loading'}
	<div class="fixed z-50" out:fade={{ delay: 500 }}>
		<PageLoader />
	</div>
{/if}

<main
	use:refresh={{
		code: 'KeyK',
		control: true,
		callback: async () => {
			await invalidateAll();
		}
	}}
>
	<slot />
</main>

<Toaster />
