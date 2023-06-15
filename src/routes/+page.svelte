<script lang="ts">
	import type { PageData } from './$types';

	import { truncate } from 'lodash';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import NavbarComponent from '$lib/components/navigation/NavbarComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';

	export let data: PageData;
</script>

<NavbarComponent />

{#if data.daily}
	<div class="homepage pb-5 pt-[4.5em]">
		<!-- daily list -->
		<div class="main-content">
			<div class="grid grid-cols-3 w-full">
				{#each data.daily as { id, attributes, relationships }}
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
			<div class="see-more w-full flex justify-center py-3">
				<a class="capitalize text-pink-400/60" href="/manga/daily">see more</a>
			</div>
		</div>

		<!-- Bookmarked -->
		<div class="main-content pt-18">
			<div class="grid grid-cols-3 w-full">
				{#each data.daily as { id, attributes, relationships }}
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
			<div class="see-more w-full flex justify-center py-3">
				<a class="capitalize text-pink-400/60" href="/">see more</a>
			</div>
		</div>
	</div>
{:else}
	<span>something went wrong, maybe check your connecton</span>
{/if}
