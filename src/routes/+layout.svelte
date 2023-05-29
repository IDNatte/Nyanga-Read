<script lang="ts">
	import { onMount } from 'svelte';
	import csrfStore from '$lib/store/csrf/csrf.store';

	onMount(() => {
		let pycsrf = document.querySelector('.pycsrf') as HTMLInputElement;
		csrfStore.set(pycsrf.value);
	});
</script>

<main>
	<a href="/testing">testing</a>

	<slot />
</main>
