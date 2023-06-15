<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { truncate } from 'lodash';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import dailyStore from '$lib/store/ephemeral/dailylist/daily.store';

	let page: number;
	$: page = 1;

	let endObserver: HTMLDivElement;

	const observer = new IntersectionObserver(
		async (event: any) => {
			if (event[0].intersectionRatio > 0.2) {
				page = ++page;
				await getNextManga(page);
			}
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: 0.2
		}
	);

	async function getMangaLists() {
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const mangaLists = await fetch(`http://localhost:5000/ipc/manga_list`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (mangaLists.status === 200) {
			const mangaData = await mangaLists.json();
			$dailyStore.data = mangaData.daily_mangalists.data;
			$dailyStore.page = page;
		} else {
			throw new Error('Something went wrong');
		}
	}

	async function getNextManga(page: number) {
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const mangaLists = await fetch(`http://localhost:5000/ipc/manga_list?page=${page}`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (mangaLists.status === 200) {
			const mangaData = await mangaLists.json();
			const prevData = $dailyStore.data;
			$dailyStore.data = [...prevData, ...mangaData.daily_mangalists.data];
		} else {
			throw new Error('Something went wrong');
		}
	}

	onMount(async () => {
		await getMangaLists();
		observer.observe(endObserver);
	});

	onDestroy(() => {
		observer.unobserve(endObserver);
		dailyStore.set({
			data: [],
			page: 0
		});
	});
</script>

<div in:fade={{ delay: 151, duration: 200 }} class="list-daily-content h-auto">
	<div class="grid grid-cols-3 w-full">
		{#each $dailyStore.data as { id, attributes, relationships }}
			<CardComponent link="/manga/detail?manga={id}">
				<div slot="card-image" class="w-full h-full">
					{#each relationships as cover}
						{#if cover.type === 'cover_art'}
							<ImageLoaderComponent
								src="https://uploads.mangadex.org/covers/{id}/{cover.attributes.fileName}"
								alt={attributes.title.en || attributes.title.ja}
							/>
						{/if}
					{/each}
				</div>

				<div slot="card-title" class="w-full flex p-5 justify-between items-center">
					<div class="flex flex-col">
						<span>{truncate(attributes.title.en || attributes.title.ja, { length: 20 })}</span>

						{#each attributes.altTitles as item}
							<span class="font-jpfont">{truncate(item.ja, { length: 15 })}</span>
						{/each}
					</div>
					{#if attributes.lastChapter && attributes.lastVolume}
						<span class="text-sm capitalize text-gray-500 bg-pink-100 rounded-full px-3 py-2"
							>ch. {attributes.lastChapter} vol. {attributes.lastVolume}</span
						>
					{/if}
				</div>
			</CardComponent>
		{/each}
	</div>
</div>
<div
	class="loader w-full h-10 bg-pink-700 text-white flex items-center justify-center"
	bind:this={endObserver}
>
	<span>loading content</span>
</div>
