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
	<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
</svg>
