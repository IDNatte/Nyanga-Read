<script lang="ts">
	export let width: string = 'w-5';
	export let height: string = 'h-5';
	export let className: string = '';
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	fill="none"
	viewBox="0 0 24 24"
	stroke-width="1.5"
	stroke="currentColor"
	class="{className} {width} {height}"
>
	<path
		stroke-linecap="round"
		stroke-linejoin="round"
		d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
	/>
</svg>
