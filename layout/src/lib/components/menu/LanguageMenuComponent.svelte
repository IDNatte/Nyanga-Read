<script lang="ts">
	import languageMenuStore from '$lib/store/languageMenu.store';

	function escapeClose(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			if ($languageMenuStore) {
				languageMenuStore.set(false);
			}
		}
	}

	function toggleMenu() {
		if (!$languageMenuStore) {
			languageMenuStore.set(true);
		} else {
			languageMenuStore.set(false);
		}
	}
</script>

<svelte:window on:keydown={escapeClose} />

<div class="relative inline-block text-left">
	<div>
		<a
			href="#!"
			class="flex w-full justify-center items-center rounded-md px-3 py-2"
			on:click|preventDefault={toggleMenu}
		>
			<slot name="title" />
		</a>
	</div>

	<div
		class="{$languageMenuStore
			? ''
			: 'hidden'} absolute right-[-24px] z-10 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
	>
		<div class="py-1">
			<slot name="content" />
		</div>
	</div>
</div>
