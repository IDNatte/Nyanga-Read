<script lang="ts">
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';
	import { Toaster } from 'svelte-french-toast';
</script>

<main class="manga-viewer">
	<slot />
</main>
<Toaster />
