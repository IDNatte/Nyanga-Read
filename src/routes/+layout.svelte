<script lang="ts">
	import type { LayoutData } from './$types';

	import { invalidateAll } from '$app/navigation';
	import { fade } from 'svelte/transition';

	import { Toaster } from 'svelte-french-toast';

	import refresh from '$lib/actions/page/refresh';
	import markdown from '$lib/utils/markdown';

	import loaderStore from '$lib/store/loader/loader.store';

	import ModalComponent from '$lib/components/modal/ModalComponent.svelte';
	import PageLoader from '$lib/components/loader/PageLoader.svelte';

	export let data: LayoutData;

	console.log(data);
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

<div class="utils">
	<!-- Toast -->
	<Toaster />

	<!-- Settings Modal -->
	<ModalComponent modal="modal-settings" title="Settings">
		{#each data.setting.preferences as { id, setting_type, value }}
			<span>{id} {setting_type} {value}</span>
		{/each}
	</ModalComponent>

	<!-- About Modal -->
	<ModalComponent modal="modal-about" title="About">
		<div class="description-wrapper p-5">
			<div class="detail w-full prose items-center max-w-full">
				{#if data.app.appInfo}
					{@html markdown(data.app.appInfo.about)}
				{/if}
			</div>
		</div>
	</ModalComponent>
</div>
