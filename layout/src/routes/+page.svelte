<script lang="ts">
	import type { PageData } from './$types';

	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { invalidateAll } from '$app/navigation';
	import mangaStore from '$lib/store/manga.store';

	import { register } from 'swiper/element/bundle';

	import RefreshComponent from '$lib/components/refresh/RefreshComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';


	export let data: PageData;

	register();

	const triggerMangaLoad = new CustomEvent('request:manga-load')
	const spaceBetween = 10;

	async function refresh() {
		await invalidateAll();
	}

	async function getMangaFromList(mangaId: string) {
		// get from https://api.mangadex.org/manga/{id}?includes[]=cover_art
		console.log(mangaId)
	}

	onMount(() => {
		document.dispatchEvent(triggerMangaLoad)
	})
</script>

<div transition:fade={{ duration: 200 }} class="content w-full h-screen">
	<!-- <pre>{JSON.stringify($mangaStore)}</pre> -->
	<div class="w-full flex fixed z-40 bg-pink-200 h-14 items-center justify-between px-3">
		<span>placeholder</span>
		<RefreshComponent on:page-refresh={refresh} />
	</div>

	<div class="main-content pt-12">
		<div class="daily-manga py-5">
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

			<div class="w-full flex justify-center">
				<!-- <span>more</span> -->
				<a
					class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
					href="/list/daily">See More</a
				>
			</div>
		</div>
	</div>

	{#if $mangaStore?.length > 0}
		{#each $mangaStore as {mangaId}}
			{#await getMangaFromList(mangaId) then data}
				<!-- promise was fulfilled -->
			{/await}
			<span>{mangaId}</span>
			 <!-- content here -->
		{/each}		
		<!-- <div class="main-content pt-12">
			<div class="bookmarked-manga py-5">
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

				<div class="w-full flex justify-center">
					<a
						class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
						href="/list/daily">See More</a
					>
				</div>
			</div>
		</div> -->
	{/if}
	<!-- <div class="main-content pt-12">
		<div class="daily-manga py-5">
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

			<div class="w-full flex justify-center">
				<a
					class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
					href="/list/daily">See More</a
				>
			</div>
		</div>
	</div> -->

</div>
