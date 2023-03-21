<script lang="ts">
	import type { PageData } from './$types';

	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { invalidateAll } from '$app/navigation';
	import mangaStore from '$lib/store/manga.store';

	import { register } from 'swiper/element/bundle';

	import RefreshComponent from '$lib/components/refresh/RefreshComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';

	export let data: PageData;

	register();

	const triggerMangaLoad = new CustomEvent('request:manga-load');
	const spaceBetween = 10;

	async function refresh() {
		await invalidateAll();
	}

	async function getMangaFromList(mangaId: string) {
		let manga = await fetch(`https://api.mangadex.org/manga/${mangaId}?includes[]=cover_art`);

		if (manga.status === 200) {
			let mangaData = await manga.json();

			return mangaData.data;
		} else {
			throw new Error('Something went wrong');
		}
	}

	onMount(() => {
		document.dispatchEvent(triggerMangaLoad);
	});
</script>

<div transition:fade={{ duration: 200 }} class="content w-full h-screen">
	<div class="w-full flex fixed z-40 bg-pink-200 h-14 items-center justify-between px-3">
		<span>placeholder</span>
		<RefreshComponent on:page-refresh={refresh} />
	</div>

	<div class="main-content pt-12">
		<div class="pb-2 pt-8 px-4 flex items-center justify-start">
			<span class="text-pink-300 text-xl uppercase underline underline-offset-4 font-light"
				>new upload</span
			>
		</div>
		<div class="daily-manga pt-5">
			<div class="slider">
				<swiper-container
					slides-per-view={3}
					space-between={spaceBetween}
					centered-slides={false}
					pagination={false}
					breakpoints={{ 768: { slidesPerView: 3 } }}
					loop={true}
					mousewheel={true}
				>
					{#each data.cover as { mangaId, mangaTitle, coverUrl, mangaAltTitles }}
						<swiper-slide>
							<div class="border shadow-md rounded">
								<a href="/read/{mangaId}">
									<ImageLoader src={coverUrl} alt={mangaTitle.en} />
									<div class="title text-center text-sm p-2">
										<div class="w-full">{mangaTitle.en}</div>
										<div class="w-full">
											{#if mangaAltTitles.length > 1}
												({#each mangaAltTitles as title}
													{#if title.ja}
														<span>{title.ja}</span>
													{/if}
												{/each})
											{/if}
										</div>
									</div>
								</a>
							</div>
						</swiper-slide>
					{/each}
				</swiper-container>
			</div>

			<div class="w-full flex justify-center py-4">
				<a
					class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
					href="/list/daily"
				>
					<span>See More</span>
				</a>
			</div>
		</div>
	</div>

	{#if $mangaStore.manga.length > 0}
		<div class="saved-manga">
			<div class="pb-2 pt-8 px-4 flex items-center justify-start">
				<span class="text-pink-300 text-xl uppercase underline underline-offset-4 font-light"
					>bookmark</span
				>
			</div>
			<div class="grid grid-cols-3">
				{#each $mangaStore.manga as { mangaId }}
					<CardComponent>
						{#await getMangaFromList(mangaId) then data}
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
						{/await}
					</CardComponent>
				{/each}
			</div>

			{#if $mangaStore.page}
				<div class="w-full flex justify-center py-4">
					<a
						class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
						href="/list/bookmark"
					>
						<span>See More</span>
					</a>
				</div>
			{/if}
		</div>
	{/if}


</div>
