<script lang="ts">
	import { page } from '$app/stores';
	import { marked } from 'marked';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';

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
			const mangaData = await manga.json();
			return mangaData.detail_data.data;
		} else {
			throw new Error('Something went wrong');
		}
	}
</script>

{#await getDetail()}
	<span>loading data</span>
{:then data}
	<div class="manga-detail">
		<div class="cover-img relative">
			{#each data.relationships as { type, attributes }}
				{#if type === 'cover_art'}
					<ImageLoaderComponent
						src="https://uploads.mangadex.org/covers/{data.id}/{attributes.fileName}"
						alt={data.attributes.title.en || data.attributes.title.ja}
						className="object-cover w-full h-96 blur-sm hover:filter-none duration-300"
					/>
				{/if}
			{/each}

			<div
				class="manga-title bg-pink-400 inline-block absolute px-3 py-2 text-white left-3 bottom-7 text-center"
			>
				<span class="block">{data.attributes.title.en || data.attributes.title.ja}</span>
				{#each data.attributes.altTitles as altTitle}
					{#if altTitle.en || altTitle.ja}
						<!-- content here -->
						<span class="block">{altTitle.en || altTitle.ja}</span>
					{/if}
				{/each}
			</div>
		</div>
		<div class="detail-content p-5">
			<div class="detail w-full prose">
				{@html marked(data.attributes.description.en, markedOpt)}
			</div>
		</div>
	</div>
{:catch error}
	<span>{error}</span>
{/await}
