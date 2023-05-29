<script lang="ts">
	import { onMount } from 'svelte';
	import csrfStore from '$lib/store/csrf/csrf.store';
	import NavbarComponent from '$lib/components/navbar/NavbarComponent.svelte';

	onMount(() => {
		let pycsrf = document.querySelector('.pycsrf') as HTMLInputElement;
		csrfStore.set(pycsrf.value);
	});
</script>

<main>
	<NavbarComponent />
	<slot />
</main>
