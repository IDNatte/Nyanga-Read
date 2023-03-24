<script lang="ts">
	import { afterUpdate, onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import dailyEphemeralStore from '$lib/store/daily.ephemeral.store';


	let initLimit: number = 9;
	let perPage: number = 3;
	let offset: number = 0;
	let limit: number = 3;

	let endObserver: HTMLDivElement;

	const observer = new IntersectionObserver(
		(event) => {
			if (event[0].intersectionRatio > 0.2) {
				limit = perPage;
				$dailyEphemeralStore.limit = limit;

				if ($dailyEphemeralStore.data.length <= 9) {
					offset = limit + initLimit;
					$dailyEphemeralStore.offset = offset;
				} else {
					offset = $dailyEphemeralStore.offset + perPage;
					$dailyEphemeralStore.offset = offset;
				}
				getManga($dailyEphemeralStore.offset, $dailyEphemeralStore.limit);
			}
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: 0.2
		}
	);



	function scrollEphemeral() {
		let lastScrollPosition = window.scrollY
		$dailyEphemeralStore.scrollPos = lastScrollPosition
	}

	async function getInitManga() {
		let mangaData = await fetch(
			'https://api.mangadex.org/manga?limit=9&offset=0&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art'
		);
		if (mangaData.status === 200) {
			let manga = await mangaData.json();
			$dailyEphemeralStore.data = manga.data;
		} else {
			throw new Error('Something went wrong :/');
		}
	}

	async function getManga(offset: number, limit: number) {
		let mangaData = await fetch(
			`https://api.mangadex.org/manga?limit=${limit}&offset=${offset}&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art`
		);

		if (mangaData.status === 200) {
			let manga = await mangaData.json();
			let data = $dailyEphemeralStore.data;
			$dailyEphemeralStore.data = [...data, ...manga.data];
		} else {
			throw new Error('Something went wrong :/');
		}
	}

	onMount(async () => {
		let scrollPos: number = $dailyEphemeralStore.scrollPos;

		if ($dailyEphemeralStore.data.length === 0) {
			await getInitManga();
		}

		setTimeout(() => {
			window.scrollTo({top: scrollPos, left: 0, behavior: 'smooth'});
		}, 2500)

		console.log($dailyEphemeralStore.scrollPos)

		observer.observe(endObserver);
	});



	onDestroy(() => {
		observer.unobserve(endObserver);
	});
</script>

<svelte:window on:scroll={scrollEphemeral} />

<div in:fade={{ duration: 200 }}>
	<div class="content grid grid-cols-3 pt-[2.2rem]">
		{#each $dailyEphemeralStore.data as { id, attributes, relationships }}
			<CardComponent>
				<a href="/read/{id}">
					{#each relationships as rel}
						{#if rel.type === 'cover_art'}
							<ImageLoader
								src={`https://uploads.mangadex.org/covers/${id}/${rel.attributes.fileName}`}
								alt={attributes.title.en}
							/>
						{/if}
					{/each}
					<div class="title text-center text-sm p-2">
						<div class="w-full">{attributes.title.en}</div>
						<div class="w-full">
							{#if attributes.altTitles.length > 1}
								({#each attributes.altTitles as title}
									{#if title.ja}
										<span>{title.ja}</span>
									{/if}
								{/each})
							{/if}
						</div>
					</div>
				</a>
			</CardComponent>
		{/each}
	</div>
	<div
		class="loader w-full h-8 bg-pink-700 text-white flex items-center justify-center"
		bind:this={endObserver}
	>
		<span>Loading Data</span>
	</div>
</div>
