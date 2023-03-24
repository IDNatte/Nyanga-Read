<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	import RefreshIcon from '$lib/components/icons/RefreshIcon.svelte';
	export let toast: any;

	const dispatch = createEventDispatcher();
</script>

<div class="flex pl-5 items-center">
	<span>Cannot load chapter image, please check your connection</span>
	<a class="px-2" href="#!" on:click|preventDefault={() => window.location.reload()}>
		<RefreshIcon width="w-5" height="h-5" />
	</a>
</div>
