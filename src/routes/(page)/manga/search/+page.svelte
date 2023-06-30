<script lang="ts">
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';

	import { debounce, truncate } from 'lodash';
	import { _ } from 'svelte-i18n';

	import searchStore from '$lib/store/ephemeral/search/search.store';

	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';
	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';

	let placeholder: boolean = true;
	let previewPage: string = '/';
	let searchValue: string;

	let data: Array<any>;
	$: data = [];

	async function searchManga(title: string) {
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const searchManga = await fetch(`http://localhost:5000/ipc/search?search=${title}`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (searchManga.status === 200) {
			const search = await searchManga.json();
			return {
				status: 'success',
				result: search.search_result.data
			};
		} else {
			return {
				status: 'error',
				result: []
			};
		}
	}

	const searchData = debounce(async (event: any) => {
		$searchStore = event.target.value;
		if (event.target.value || event.target.value !== '') {
			searchValue = event.target.value;
			placeholder = false;

			const search = await searchManga(searchValue);
			if (search.status === 'success') {
				data = search.result;
			} else {
				data = [];
			}
		} else {
			placeholder = true;
			searchValue = '';
			data = [];
		}
	}, 300);

	onMount(async () => {
		if ($searchStore) {
			const search = await searchManga($searchStore);
			searchValue = $searchStore;
			placeholder = false;

			if (search.status === 'success') {
				data = [...data, ...search.result];
			} else {
				data = [];
			}
		}
	});

	afterNavigate(({ from }) => {
		if (from?.url.pathname === '/manga/read') {
			previewPage = '/';
		} else {
			previewPage = from?.url.pathname || previewPage;
		}
	});
</script>

<div class="search-page p-5">
	<div class="searchbox">
		<input
			on:input={searchData}
			type="text"
			class="border px-2 py-1 rounded w-full"
			placeholder={$_('page.searchPage.searchPlaceholder')}
			bind:value={$searchStore}
		/>
	</div>
	<div class="search-result w-full pt-8">
		{#if placeholder}
			<div class="w-full text-center">
				<span class="italic text-gray-400 text-xl">{$_('page.searchPage.searchContainer')} </span>
				<span class="text-xl pl-1">😸</span>
			</div>
		{/if}
		{#if data.length !== 0}
			<div class="grid grid-cols-3 w-full">
				{#each data as { attributes, relationships, id }}
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

								<!-- UI bug if duplicate key occured -->
								{#each attributes.altTitles as item}
									{#if item.ja}
										<span class="font-jpfont">
											{truncate(item.ja, { length: 15 })}
										</span>
									{/if}
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
		{/if}
		{#if searchValue && data.length === 0}
			<div class="w-full text-center">
				<span class="italic text-gray-400 text-xl">
					{$_('page.searchPage.nothingFound')} "{searchValue}"
				</span>
				<span class="text-xl pl-1">😿</span>
			</div>
		{/if}
	</div>
</div>

<FloatNavigationComponent showBookmark={false} showBack={false} homeUrl="/" />
