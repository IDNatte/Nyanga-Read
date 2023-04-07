<script lang="ts">
	import { _ } from 'svelte-i18n';

	import RefreshIcon from '$lib/components/icons/RefreshIcon.svelte';
	export let toast: any;
</script>

<div class="flex pl-5 items-center">
	<span>{$_('error.imgLoadErr')}</span>
	<a class="px-2" href="#!" on:click|preventDefault={() => window.location.reload()}>
		<RefreshIcon width="w-5" height="h-5" />
	</a>
</div>
