<script lang="ts">
	import NavbarComponent from '$lib/components/navigation/NavbarComponent.svelte';
</script>

<main>
	<NavbarComponent />
	<div class="pt-[4.5em]">
		<slot />
	</div>
</main>
