<script lang="ts">
	import dropdownStore from '$lib/store/dropdown/dropdown.store';
	import outsideClick from '$lib/actions/dropdown/outsideclick';

	export let className: string = 'right-0 top-8';
	export let width: string = 'w-[14em]';
	export let dropdown: string;
</script>

{#if $dropdownStore.dropdown === dropdown && $dropdownStore.open}
	<div
		use:outsideClick
		class="dropdown {$dropdownStore.open
			? 'block'
			: 'hidden'} absolute {className} {width} bg-white py-4 rounded border border-gray-100 shadow-lg"
	>
		<slot />
	</div>
{/if}
