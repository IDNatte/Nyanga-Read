<script lang="ts">
	import { truncate } from 'lodash';

	// debug
	import mainStore from '$lib/store/ephemeral/main/main.store';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import NavbarComponent from '$lib/components/navigation/NavbarComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import BookIcon from '$lib/components/icons/BookIcon.svelte';
</script>

<NavbarComponent />

<div class="homepage pb-5 pt-[4.5em]">
	<!-- daily list -->
	<div class="daily-content">
		{#if $mainStore.daily.length !== 0}
			<div class="w-full px-6 py-5 flex items-center">
				<div class="relative p-2 rounded-full bg-pink-100">
					<div class="animate-ping border-2 p-2 rounded-full border-white absolute" />
					<BookIcon className="fill-pink-400 relative" />
				</div>
				<span class="text-xl capitalize text-pink-400 pl-3 underline underline-offset-2"
					>Daily Manga</span
				>
			</div>
			<div class="grid grid-cols-3 w-full">
				{#each $mainStore.daily as { id, attributes, relationships }}
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
				<a
					class="capitalize text-pink-400/60 text-xl underline underline-offset-2"
					href="/manga/daily">see more</a
				>
			</div>
		{/if}
	</div>

	<!-- Bookmarked -->
	{#if $mainStore.bookmark.length !== 0}
		<div class="bookmarked-content pt-18">
			<div class="w-full px-6 py-5 flex items-center">
				<div class="relative p-2 rounded-full bg-pink-100">
					<div class="animate-ping border-2 p-2 rounded-full border-white absolute" />
					<BookmarkIcon className="fill-pink-400 relative stroke-pink-400" />
				</div>
				<span class="text-xl capitalize text-pink-400 pl-3 underline underline-offset-2"
					>my bookmark</span
				>
			</div>
			<div class="grid grid-cols-3 w-full">
				{#each $mainStore.bookmark as { id, attributes, relationships }}
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
				<a class="capitalize text-pink-400/60 text-xl underline underline-offset-2" href="/"
					>see more</a
				>
			</div>
		</div>
	{/if}
</div>

{#if $mainStore.daily.length === 0 && $mainStore.bookmark.length === 0}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">something went wrong..!!</span>
	</div>
{/if}
