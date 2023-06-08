<script lang="ts">
	import { page } from '$app/stores';
	import { json } from '@sveltejs/kit';
	import { marked } from 'marked';

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
		}
	}
</script>

<div>testing</div>

{#await getDetail()}
	<span>loading data</span>
{:then data}
	<div class="manga-detail">
		<div class="cover-img">
			<span>here lies cover</span>
		</div>
		<div class="prose">
			{@html marked(data.attributes.description.en, markedOpt)}
		</div>
	</div>
{/await}
