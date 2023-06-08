<script lang="ts">
	import type { PageData } from './$types';
	import { marked } from 'marked';

	export let data: PageData;

	const markedOpt = {
		smartLists: true,
		smartypants: true,
		gfm: true,
		breaks: false
	};
</script>

<div class="manga-detail">
	<div class="cover-img">
		<span>here lies cover</span>
	</div>
	<div class="prose">
		{@html marked(data.manga.attributes.description.en, markedOpt)}
	</div>
</div>
