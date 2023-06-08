<script lang="ts">
	import { onMount } from 'svelte';
	import { invalidateAll } from '$app/navigation';
	import { fade } from 'svelte/transition';

	import refresh from '$lib/actions/page/refresh';
	import csrfStore from '$lib/store/csrf/csrf.store';
	import loaderStore from '$lib/store/loader/loader.store';

	import NavbarComponent from '$lib/components/navbar/NavbarComponent.svelte';
	import PageLoader from '$lib/components/loader/PageLoader.svelte';

	onMount(() => {
		let pycsrf = document.querySelector('.pycsrf') as HTMLInputElement;
		csrfStore.set(pycsrf.value);
	});
</script>

{#if $loaderStore === 'loading'}
	<div out:fade={{ delay: 500 }}>
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
	<NavbarComponent />
	<div class="pt-[4.5em]">
		<slot />
	</div>
</main>
