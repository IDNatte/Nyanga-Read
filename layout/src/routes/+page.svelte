<script lang="ts">
	import type { PageData } from './$types';
	import {invalidateAll} from '$app/navigation'
	import RefreshComponent from '$lib/components/refresh/RefreshComponent.svelte';

	export let data: PageData;

	async function refresh() {
		await invalidateAll()
	}
</script>

<div>
	<div class="refresher">
		<RefreshComponent on:page-refresh={refresh} />
	</div>
	<ul>
		{#each data.cover as { mangaId, mangaTitle, coverUrl, mangaAltTitles }}
			<li>
				<a href="/read/{mangaId}">
					<div>
						<span>{mangaTitle.en}</span>
						({#each mangaAltTitles as title}
							{#if title.ja}
								<span>{title.ja}</span>,
							{/if}
							{#if title.en}
							<span>{title.en}</span>,
						{/if}
						{/each})</div>
					<img class="cover-img" src={coverUrl} alt="" srcset="" />
				</a>
			</li>
		{/each}
	</ul>
</div>



<style>
	.cover-img {
		width: 100%;
	}

	.refresher {
		display: block;
		position: fixed;
		bottom: 2em;
		right: 2em;
	}
</style>
