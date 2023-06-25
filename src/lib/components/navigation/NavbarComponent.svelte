<script lang="ts">
	import { invalidateAll } from '$app/navigation';

	import dropdownStore from '$lib/store/dropdown/dropdown.store';

	import DropdownComponent from '$lib/components/dropdown/DropdownComponent.svelte';

	import MagniglassIcon from '$lib/components/icons/MagniglassIcon.svelte';
	import TransalateIcon from '$lib/components/icons/TransalateIcon.svelte';
	import VerticalIcon from '$lib/components/icons/VerticalIcon.svelte';
	import SettingsIcon from '$lib/components/icons/SettingsIcon.svelte';
	import RefreshIcon from '$lib/components/icons/RefreshIcon.svelte';
	import NavbarIcon from '$lib/components/icons/NavbarIcon.svelte';
	import InfoIcon from '$lib/components/icons/InfoIcon.svelte';
	import modalStore from '$lib/store/modal/modal.store';

	function dropdownClick() {
		if ($dropdownStore) {
			$dropdownStore = false;
		} else {
			$dropdownStore = true;
		}
	}

	function openModal(modal: string) {
		modalStore.set({ modal: modal, open: true });
	}
</script>

<nav
	class="navbar w-full bg-pink-300 flex flex-row items-center justify-between px-2 text-gray-900 fixed z-50"
>
	<div class="py-2 pl-2">
		<NavbarIcon width="w-[56px]" height="h-auto" />
	</div>
	<div class="pr-5">
		<div class="dropdown-wrapper relative">
			<button
				class="menu-dropdown px-5 py-2 rounded border border-transparent transition duration-150 ease-in-out hover:shadow hover:border-white/30"
				on:click={dropdownClick}
			>
				<VerticalIcon />
			</button>
			<DropdownComponent top="top-12">
				<ul>
					<li>
						<a
							href="/manga/search"
							on:click={() => {
								dropdownStore.set(false);
							}}
						>
							<MagniglassIcon width="w-5" height="w-5" />
							<span>Search</span>
						</a>
					</li>
					<li>
						<a
							href="#!"
							on:click|preventDefault={() => {
								dropdownStore.set(false);
								openModal('modal-settings');
							}}
						>
							<SettingsIcon width="w-5" height="w-5" />
							<span>Settings</span>
						</a>
					</li>

					<li>
						<a
							href="/#!"
							on:click|preventDefault={async () => {
								dropdownStore.set(false);
								await invalidateAll();
							}}
						>
							<RefreshIcon width="w-5" height="w-5" />
							<span>Reload Page</span>
						</a>
					</li>
					<li>
						<a
							href="#!"
							on:click|preventDefault={() => {
								dropdownStore.set(false);
								openModal('modal-about');
							}}
						>
							<InfoIcon width="w-5" height="w-5" />
							<span>About Application</span>
						</a>
					</li>
				</ul>
			</DropdownComponent>
		</div>
	</div>
</nav>

<style lang="postcss">
	ul {
		@apply divide-y;
	}

	ul li a {
		@apply w-full py-2 px-3 font-light capitalize flex items-center;
	}

	ul li a span {
		@apply pl-5;
	}
</style>
