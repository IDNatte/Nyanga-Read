<script>
	import dropdownStore from '$lib/store/dropdown/dropdown.store';

	import DropdownComponent from '$lib/components/dropdown/DropdownComponent.svelte';
	import VerticalIcon from '$lib/components/icons/VerticalIcon.svelte';
	import NavbarIcon from '$lib/components/icons/NavbarIcon.svelte';
	import MagniglassIcon from '$lib/components/icons/MagniglassIcon.svelte';
	import RefreshIcon from '$lib/components/icons/RefreshIcon.svelte';
	import TransalateIcon from '$lib/components/icons/TransalateIcon.svelte';
	import InfoIcon from '$lib/components/icons/InfoIcon.svelte';

	function dropdownClick() {
		if ($dropdownStore) {
			$dropdownStore = false;
		} else {
			$dropdownStore = true;
		}
	}
</script>

<nav
	class="navbar w-full bg-pink-300 flex flex-row items-center justify-between px-2 text-gray-900 fixed"
>
	<a class="py-2" href="/">
		<NavbarIcon width="w-[300px]" height="h-auto" />
	</a>
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
						<a href="/testing">
							<MagniglassIcon width="w-5" height="w-5" />
							<span>Search</span>
						</a>
					</li>
					<li>
						<a href="/testing">
							<RefreshIcon width="w-5" height="w-5" />
							<span>Reload Page</span>
						</a>
					</li>
					<li>
						<a href="/testing">
							<TransalateIcon width="w-5" height="w-5" />
							<span>Select language</span>
						</a>
					</li>
					<li>
						<a href="/testing">
							<InfoIcon width="w-5" height="w-5" />
							<span>About Application</span>
						</a>
					</li>
				</ul>
			</DropdownComponent>
		</div>
	</div>
</nav>

<style>
	ul {
		@apply divide-y;
	}

	ul li a {
		@apply w-full block py-2 px-3 font-light capitalize flex items-center;
	}

	ul li a span {
		@apply pl-5;
	}
</style>
