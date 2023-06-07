<script lang="ts">
	import { onMount } from 'svelte';
	import { invalidateAll } from '$app/navigation';

	import refresh from '$lib/actions/page/refresh';
	import csrfStore from '$lib/store/csrf/csrf.store';
	import NavbarComponent from '$lib/components/navbar/NavbarComponent.svelte';

	onMount(() => {
		let pycsrf = document.querySelector('.pycsrf') as HTMLInputElement;
		csrfStore.set(pycsrf.value);
	});
</script>

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
	<slot />
</main>
