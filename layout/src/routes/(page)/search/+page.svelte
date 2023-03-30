<script lang="ts">
	import { fade } from 'svelte/transition';

	import { _ } from 'svelte-i18n';
	import { debounce, truncate } from 'lodash';

	import searchEphemeralStore, {
		type SearchEphemeralType
	} from '$lib/store/search.ephemeral.store';

	import CircleLoaderComponent from '$lib/components/loader/CircleLoaderComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import { onMount } from 'svelte';

	let loading: boolean = false;
	let searchboxPlaceholder: boolean = true;

	let data: Array<any> = [];
	$: data = [];

	let searchBoxText: SearchEphemeralType = $searchEphemeralStore;

	async function searchManga(title: string) {
		loading = true;
		let manga = await fetch(
			`https://api.mangadex.org/manga?title=${title}&originalLanguage[]=ja&includes[]=cover_art&availableTranslatedLanguage[]=${document.documentElement.lang}&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&`
		);

		if (manga.status === 200) {
			loading = false;
			let searchManga = await manga.json();

			return searchManga;
		} else {
			loading = false;
			return { error: true, message: 'something went wrong' };
		}
	}

	const searchData = debounce(async (event: any) => {
		data = [];
		searchboxPlaceholder = false;
		searchEphemeralStore.set(event.target.value);

		if (event.target.value || event.target.value !== '') {
			let mangaSearchReasult = await searchManga(event.target.value);
			data = mangaSearchReasult.data;
		} else {
			data = [];
			loading = false;
			searchboxPlaceholder = true;
		}
	}, 500);

	onMount(async () => {
		if (searchBoxText !== null) {
			searchboxPlaceholder = false;
			let mangaSearchReasult = await searchManga(searchBoxText);
			data = mangaSearchReasult.data;
		}
	});
</script>

<div in:fade={{ duration: 200 }} class="search-page pt-[2.2rem]">
	<div class="search-content flex w-full fixed p-5 bg-pink-300 z-40 shadow">
		<input
			type="text"
			on:input={searchData}
			placeholder={$_('search.searchBoxPlaceholder')}
			class="searchbox border w-full bg-transparent rounded p-1 font-light text-white duration-300 focus:outline-none"
			bind:value={searchBoxText}
		/>
	</div>
	<div class="search-content pt-24 px-5 pb-5">
		{#if loading}
			<CircleLoaderComponent
				style={{ className: 'flex items-center justify-center', h: 'h-20', w: 'w-20' }}
			/>
		{/if}

		{#if searchboxPlaceholder}
			<div class="w-full text-center">
				<div class="text-gray-400">
					<span class="italic font-thin text-lg capitalize">{$_('search.searchContent')}</span>
					<span class="text-lg">🤔</span>
				</div>
			</div>
		{/if}

		{#if !searchboxPlaceholder && !loading && data.length === 0}
			<div class="w-full text-center">
				<div class="text-gray-400">
					<span class="italic font-thin text-lg capitalize"
						>{$_('search.searchContentEmpty', { values: { title: searchBoxText } })}</span
					>
					<span class="text-lg">🫤</span>
				</div>
			</div>
		{/if}

		<div class="grid grid-cols-3">
			{#each data as { id, attributes, relationships }}
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
						<div class="title text-center text-xs p-2">
							<div class="w-full">
								{truncate(attributes.title.en || attributes.title.ja, { length: 20 })}
							</div>
							<div class="w-full">
								{#if attributes.altTitles.length > 1}
									({#each attributes.altTitles as title}
										{#if title.ja}
											<span>{truncate(title.ja, { length: 20 })}</span>
										{/if}
									{/each})
								{/if}
							</div>
						</div>
					</a>
				</CardComponent>
			{/each}
		</div>
	</div>
</div>

<style lang="postcss">
	.searchbox::-webkit-input-placeholder {
		@apply text-white italic text-sm;
	}
</style>
