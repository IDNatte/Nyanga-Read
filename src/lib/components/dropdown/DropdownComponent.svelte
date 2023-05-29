<script lang="ts">
	import dropdownStore from '$lib/store/dropdown/dropdown.store';

	export let width: string = 'w-[14em]';
	export let top: string = 'top-8';
</script>

<div
	class="dropdown {$dropdownStore
		? 'block'
		: 'hidden'} absolute right-0 {width} bg-white py-4 rounded {top} border border-gray-100 shadow-lg"
>
	<slot />
</div>
