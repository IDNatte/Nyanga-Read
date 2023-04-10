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
<img
	src="https://uploads.mangadex.org/covers/192aa767-2479-42c1-9780-8d65a2efd36a/bd11738f-e13d-4d76-8777-3440d6f2b6a7.jpg"
	alt=""
/>

<!-- <ul>
	{#each data as { cover }}
		<li>
			<img
				src="https://uploads.mangadex.org/covers/192aa767-2479-42c1-9780-8d65a2efd36a/bd11738f-e13d-4d76-8777-3440d6f2b6a7.jpg"
				alt=""
			/>
		</li>
	{/each}
</ul> -->
