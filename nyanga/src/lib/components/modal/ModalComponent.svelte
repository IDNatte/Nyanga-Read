<script lang="ts">
	import { fade } from 'svelte/transition';

	import outsideClick from '$lib/actions/modal/outsideclick';
	import modalStore from '$lib/store/modal/modal.store';

	import CloseIcon from '$lib/components/icons/CloseIcon.svelte';

	export let modal: string;
	export let title: string;
	export let height: string = 'h-2/3';
	export let width: string = ' w-2/3 ';
	export let className: string = '';

	function escapeClose(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			if ($modalStore.modal === modal && $modalStore.open) {
				modalStore.set({ modal: null, open: false });
			}
		}
	}

	function close() {
		modalStore.set({ modal: null, open: false });
	}
</script>

<svelte:window on:keydown={escapeClose} />

{#if $modalStore.modal === modal && $modalStore.open}
	<div
		transition:fade|global={{ duration: 300 }}
		class="{modal} {className} block w-full h-screen z-50 fixed top-0"
	>
		<div class="flex items-center justify-center w-full h-screen bg-pink-200/60">
			<div use:outsideClick class="modal-content bg-white rounded {width} {height} overflow-x-auto">
				<div
					class="modal-title px-4 py-5 fixed bg-white {width} border-b flex items-center justify-between rounded-t"
				>
					<span class="text-lg font-thin capitalize">{title}</span>
					<a href="#!" on:click|preventDefault={close}><CloseIcon /></a>
				</div>
				<div class="content p-5 mt-[4.3rem]">
					<slot />
				</div>
			</div>
		</div>
	</div>
{/if}
