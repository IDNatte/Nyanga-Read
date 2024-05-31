<script lang="ts">
	import { fade } from 'svelte/transition';

	import { get as get_, truncate } from 'lodash';
	import { _ } from 'svelte-i18n';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';

	async function getBookmark() {
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const bookmark = await fetch(`http://localhost:5000/ipc/bookmark`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (bookmark.status === 200) {
			const bookmarkData = await bookmark.json();
			return bookmarkData.bookmark;
		} else {
			throw new Error('something went error !');
		}
	}
</script>

{#await getBookmark()}
	<div in:fade|global={{ duration: 200 }} out:fade|global={{ duration: 150 }}>
		<CirclePageLoader
			color="text-pink-700"
			style={{
				className: 'w-full h-screen flex items-center justify-center',
				w: 'w-10',
				h: 'h-10'
			}}
		/>
	</div>
{:then data}
	<div in:fade|global={{ delay: 151, duration: 200 }} class="manga-detail">
		<div class="grid grid-cols-3 w-full">
			{#each data as { id, attributes, relationships }}
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
							<span
								>{truncate(attributes.title.en, { length: 20 }) ||
									truncate(get_(attributes.title, 'ja-ro'), { length: 20 }) ||
									truncate(attributes.title.ja, { length: 20 })}</span
							>

							<!-- UI bug if duplicate key occured -->
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
{:catch error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">{$_('page.bookmarkPage.error.notif')}..!!</span>
	</div>
{/await}

<FloatNavigationComponent showBookmark={false} showBack={false} homeUrl="/" />
