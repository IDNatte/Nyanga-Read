<script lang="ts">
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';

	import { marked } from 'marked';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';

	const markedOpt = {
		smartLists: true,
		smartypants: true,
		gfm: true,
		breaks: false
	};

	async function getDetail() {
		const mangaId = $page.url.searchParams.get('manga');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const manga = await fetch(`http://localhost:5000/ipc/get_detail/${mangaId}`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (manga.status === 200) {
			const mangaDetail = await manga.json();
			console.log(mangaDetail.detail_data.data);
			return {
				detail: mangaDetail.detail_data.data,
				mangaLists: mangaDetail.manga_data
			};
		} else {
			throw new Error('Something went wrong');
		}
	}
</script>

{#await getDetail()}
	<div in:fade={{ duration: 200 }} out:fade={{ duration: 150 }}>
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
	<div in:fade={{ delay: 151, duration: 200 }} class="manga-detail">
		<div class="cover-img relative">
			{#each data.detail.relationships as { type, attributes }}
				{#if type === 'cover_art'}
					<ImageLoaderComponent
						src="https://uploads.mangadex.org/covers/{data.detail.id}/{attributes.fileName}"
						alt={data.detail.attributes.title.en || data.detail.attributes.title.ja}
						className="object-cover w-full h-96 blur-sm hover:filter-none duration-300"
					/>
				{/if}
			{/each}

			<div
				class="manga-title bg-pink-400 inline-block absolute px-3 py-2 text-white left-3 bottom-7 text-center"
			>
				<span class="block"
					>{data.detail.attributes.title.en || data.detail.attributes.title.ja}</span
				>
				{#each data.detail.attributes.altTitles as altTitle}
					{#if altTitle.en || altTitle.ja}
						<!-- content here -->
						<span class="block">{altTitle.en || altTitle.ja}</span>
					{/if}
				{/each}
			</div>
		</div>
		<div class="detail-content divide-y-2">
			<div class="content-wrapper p-5">
				{#if data.detail.attributes.description.en}
					<div class="detail w-full prose items-center max-w-full">
						{@html marked(data.detail.attributes.description.en, markedOpt)}
					</div>
				{:else}
					<div class="detail w-full text-center">
						<span>No Description 😕</span>
					</div>
				{/if}
			</div>
			<div class="content-wrapper p-5">
				<div class="chapter-list">
					<ul>
						{#each data.mangaLists as { chapter, chapter_id }}
							<li>
								<a href="/manga/read?chapter={chapter_id}">{chapter}</a>
							</li>
						{/each}
					</ul>
				</div>
			</div>
		</div>
	</div>
{:catch error}
	<span>{error}</span>
{/await}
