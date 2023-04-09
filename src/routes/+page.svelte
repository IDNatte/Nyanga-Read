<script lang="ts">
	import { onMount } from 'svelte';

	let data: Array<any>;
	$: data = [];

	onMount(() => {
		const triggerInitManga = new CustomEvent('request:init-manga', {
			detail: { lang: document.documentElement.lang }
		});

		document.dispatchEvent(triggerInitManga);

		document.addEventListener('load:init-manga', (event: any) => {
			data = [...data, ...event.detail];
		});
	});
</script>

<span>Here is main Page</span>
<ul>
	{#each data as { cover }}
		<li>
			<img src={cover.localUrl} alt="" />
		</li>
	{/each}
</ul>
