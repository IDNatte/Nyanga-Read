<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import bookmarkStore from '$lib/store/bookmark.store';

	const triggerLoadAllBookmark = new CustomEvent('request:manga-load-all');

	async function getManga(mangaId: string) {
		let manga = await fetch(`https://api.mangadex.org/manga/${mangaId}?includes[]=cover_art`);

		if (manga.status === 200) {
			let mangaData = await manga.json();

			return mangaData.data;
		} else {
			throw new Error('Something went wrong');
		}
	}

	onMount(() => {
		document.dispatchEvent(triggerLoadAllBookmark);

		document.addEventListener('manga-action:load-all', (event: any) => {
			bookmarkStore.set(event.detail.data);
		});
	});
</script>

<div in:fade={{ duration: 200 }}>
	<div class="bookmark-list grid grid-cols-3 pt-[2.2rem]">
		{#each $bookmarkStore.manga as { mangaId }}
			{#await getManga(mangaId) then data}
				<CardComponent>
					<a href="/read/{mangaId}">
						{#each data.relationships as rel}
							{#if rel.type === 'cover_art'}
								<ImageLoader
									src={`https://uploads.mangadex.org/covers/${data.id}/${rel.attributes.fileName}`}
									alt={data.id}
								/>
							{/if}
						{/each}
						<div class="title text-center text-sm p-2">
							<div class="w-full">{data.attributes.title.en || data.attributes.title.ja}</div>
							<div class="w-full">
								{#if data.attributes.altTitles.length > 1}
									({#each data.attributes.altTitles as altTtitle}
										{#if altTtitle.ja}
											<span>{altTtitle.ja}</span>
										{/if}
									{/each})
								{/if}
							</div>
						</div>
					</a>
				</CardComponent>
			{/await}
		{/each}
	</div>
</div>
