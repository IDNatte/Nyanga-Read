<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<ul>
	{#each data.volume as { volume, chapter }}
		<li>
			<div>Volume {volume}</div>
			<ul>
				{#each chapter as { chapterId, chapterName }}
					<li><a href="/read/{data.mangaId}/{chapterId}">Chapter {chapterName}</a></li>
				{/each}
			</ul>
		</li>
	{/each}
</ul>
