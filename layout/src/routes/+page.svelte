<script lang="ts">
	import type { PageData } from './$types';
	
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { invalidateAll } from '$app/navigation';

	import { register } from 'swiper/element/bundle';
	import { _ } from 'svelte-i18n'

	import bookmarkStore from '$lib/store/bookmark.store';
	import modalStore from '$lib/store/modal.store';
	import menuStore from '$lib/store/menu.store';

	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import NavbarIcon from '$lib/components/icons/NavbarIcon.svelte';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import MenuComponent from '$lib/components/menu/MenuComponent.svelte';

	import MagniglassIcon from '$lib/components/icons/MagniglassIcon.svelte';
	import TransalateIcon from '$lib/components/icons/TransalateIcon.svelte';
	import UpdateAppIcon from '$lib/components/icons/UpdateAppIcon.svelte';
	import RefreshIcon from '$lib/components/icons/RefreshIcon.svelte';
	import InfoIcon from '$lib/components/icons/InfoIcon.svelte';

	export let data: PageData;

	register();

	const triggerMangaLoad = new CustomEvent('request:manga-load');
	const triggerAppUpdate = new CustomEvent('request:app-update');
	const spaceBetween = 10;

	function openAbout(modal: string) {
		modalStore.set({ modal: modal, open: true });
	}

	function openUpdate(modal: string) {
		document.dispatchEvent(triggerAppUpdate);
		modalStore.set({ modal: modal, open: true });
	}

	function openLanguage(modal: string) {
		modalStore.set({ modal: modal, open: true });
	}

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

<div in:fade={{ duration: 200 }} class="content w-full pt-[2.2rem]">
	{#if data.manga.status !== 'error' && data.cover.length !== 0}
		<div
			class="w-full flex fixed z-30 bg-pink-300 h-14 shadow items-center justify-between px-3 top-[2.2rem]"
		>
			<NavbarIcon width="w-[200px]" />
			<MenuComponent>
				<div class="divide-y font-thin text-sm">
					<!-- common menu -->
					<div class="common">
						<a
							href="/search"
							on:click={() => menuStore.set(false)}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<MagniglassIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">{$_('menu.search')}</span>
						</a>
						<a
							href="#!"
							on:click|preventDefault={() => {
								menuStore.set(false);
								refresh();
							}}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<RefreshIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">{$_('menu.reload')}</span>
						</a>
					</div>

					<!-- language menu -->
					<div class="about">
						<a
							href="#!"
							on:click|preventDefault={() => {
								menuStore.set(false);
								openLanguage('language-modal');
							}}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<TransalateIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">{$_('menu.langSelect')}</span>
						</a>
					</div>

					<!-- About menu -->
					<div class="about">
						<a
							href="#!"
							on:click|preventDefault={() => {
								menuStore.set(false);
								openAbout('about-modal');
							}}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<InfoIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">{$_('menu.about')}</span>
						</a>
						<a
							href="#!"
							on:click|preventDefault={() => {
								menuStore.set(false);
								openUpdate('update-modal');
							}}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<UpdateAppIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">{$_('menu.update')}</span>
						</a>
					</div>

					<!-- debug -->
					<div class="about">
						<a
							href="/road/to/nowhere"
							on:click={() => {
								menuStore.set(false);
							}}
							class="text-gray-700 px-4 py-2 flex items-center"
						>
							<div class="logo pl-1 pr-3">
								<UpdateAppIcon
									width="w-5"
									height="h-auto"
									className="flex items-center justify-center"
								/>
							</div>
							<span class="capitalize">debug</span>
						</a>
					</div>
				</div>
			</MenuComponent>
		</div>

		<div class="main-content pt-14 overflow-auto">
			<div class="pb-2 pt-8 px-4 flex items-center justify-start">
				<span class="text-pink-300 text-xl uppercase underline underline-offset-4 font-light"
					>{$_('mainPage.newUpload')}</span
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
											<div class="w-full">{mangaTitle.en || mangaTitle.ja}</div>
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
						<span class="capitalize">{$_('mainPage.seeMore')}</span>
					</a>
				</div>
			</div>
		</div>

		{#if $bookmarkStore.manga.length > 0}
			<div class="saved-manga">
				<div class="pb-2 pt-5 px-4 flex items-center justify-start">
					<span class="text-pink-300 text-xl uppercase underline underline-offset-4 font-light"
						>{$_('mainPage.bookmark')}</span
					>
				</div>
				<div class="grid grid-cols-3">
					{#each $bookmarkStore.manga as { mangaId }}
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

				{#if $bookmarkStore.page}
					<div class="w-full flex justify-center py-4">
						<a
							class="text-pink-300 underline underline-offset-4 font-light text-lg py-2"
							href="/list/bookmark"
						>
							<span class="capitalize">{$_('mainPage.seeMore')}</span>
						</a>
					</div>
				{/if}
			</div>
		{/if}
	{/if}

	{#if data.manga.status === 'error' && data.cover.length === 0}
		<div class="flex items-center h-screen w-full justify-center flex-col">
			<span class="text-8xl pb-8">😿</span>
			<span class="font-light">{$_('error.networkError.text1')}</span>
			<span class="font-light">{$_('error.networkError.text2')}</span>
			<a class="underline" href="#!" on:click|preventDefault={() => window.location.reload()}
				>{$_('error.networkError.reload')}</a
			>
		</div>
	{/if}
</div>
