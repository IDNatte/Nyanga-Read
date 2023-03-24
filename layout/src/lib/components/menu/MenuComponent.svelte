<script lang="ts">
	import VerticalIcon from '$lib/components/icons/VerticalIcon.svelte';
	import menuStore from '$lib/store/menu.store';

	function escapeClose(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			if ($menuStore) {
				menuStore.set(false);
			}
		}
	}

	function toggleMenu() {
		if (!$menuStore) {
			menuStore.set(true);
		} else {
			menuStore.set(false);
		}
	}
</script>

<svelte:window on:keydown={escapeClose} />

<div class="relative inline-block text-left">
	<div>
		<a
			href="#!"
			class="inline-flex w-full justify-center gap-x-1.5 rounded-md px-3 py-2"
			on:click|preventDefault={toggleMenu}
		>
			<VerticalIcon />
		</a>
	</div>

	<div
		class="{$menuStore
			? ''
			: 'hidden'} absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
	>
		<div class="py-1">
			<slot />
		</div>
	</div>
</div>
