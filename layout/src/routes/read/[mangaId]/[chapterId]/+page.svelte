<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	console.log(data.chapter);
</script>

<ul>
	{#each data.chapter as { url }}
		<img src={url} alt="" />
	{/each}
</ul>

<style>
	img {
		width: 100%;
	}
</style>
