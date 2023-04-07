<script lang="ts">
	import { fade } from 'svelte/transition';

	import modalStore from '$lib/store/modal.store';

	import CloseIcon from '$lib/components/icons/CloseIcon.svelte';

	export let modal: string;
	export let title: string;

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
	<div transition:fade={{ duration: 300 }} class="{modal} block w-full h-screen z-50 fixed top-0">
		<div class="flex items-center justify-center w-full h-screen bg-pink-200/60">
			<div class="modal-content bg-white rounded w-2/3 h-2/3 overflow-x-auto">
				<div
					class="modal-title px-4 py-5 fixed bg-white w-2/3 border-b flex items-center justify-between rounded-t"
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
