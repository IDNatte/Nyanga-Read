<script lang="ts">
	import type { PageData } from './$types';

	import { truncate } from 'lodash';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';

	export let data: PageData;
</script>

<div class="homepage pb-5">
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

					<div
						slot="card-title"
						class="w-full flex justify-center p-5 flex-col items-center text-center"
					>
						<span>{truncate(attributes.title.en || attributes.title.ja, { length: 20 })}</span>

						{#each attributes.altTitles as item}
							<span class="font-jpfont">{truncate(item.ja, { length: 30 })}</span>
						{/each}
					</div>
				</CardComponent>
			{/each}
		</div>
		<div class="see-more w-full flex justify-center">
			<a class="capitalize text-pink-400/60" href="/">see more</a>
		</div>
	</div>

	<div class="main-content pt-20">
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
					<div
						slot="card-title"
						class="w-full flex justify-center p-5 flex-col items-center text-center"
					>
						<span>{truncate(attributes.title.en || attributes.title.ja, { length: 20 })}</span>

						{#each attributes.altTitles as item}
							<span class="font-jpfont">{truncate(item.ja, { length: 20 })}</span>
						{/each}
					</div>
				</CardComponent>
			{/each}
		</div>
		<div class="see-more w-full flex justify-center">
			<a class="capitalize text-pink-400/60" href="/">see more</a>
		</div>
	</div>
</div>
