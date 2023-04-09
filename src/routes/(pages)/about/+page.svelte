<script lang="ts">
	import { VERSION } from 'svelte/compiler';
	import { onMount } from 'svelte';

	onMount(() => {
		const triggerTest = new CustomEvent('send:frontend-version', { detail: { version: VERSION } });
		document.dispatchEvent(triggerTest);
	});
</script>

<span>{VERSION}</span>
