<script lang="ts">
	import type { PageData } from './$types';
	import { beforeNavigate } from '$app/navigation';
	import { fade } from 'svelte/transition';
	
	import AccordionComponent from '$lib/components/accordion/AccordionComponent.svelte';
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import accordionStore from '$lib/store/accordion.store';
	
	export let data: PageData;

	beforeNavigate(() => {
		accordionStore.set({accordionOpen: null, accordionId: null})
	})
</script>

<div transition:fade={{duration: 200}}>
	{#each data.volume as { volume, chapter }}
		<CardComponent>
			<AccordionComponent title={`volume ${volume}`}>
				<ul class="divide-y">
					{#each chapter as { chapterId, chapterName }}
						<li class="py-2 block">
							<a class="px-4 w-full block" href="/read/{data.mangaId}/{chapterId}">Chapter {chapterName}</a>
						</li>
					{/each}
				</ul>
			</AccordionComponent>
		</CardComponent>
	{/each}
</div>

<!-- <ul>
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
</ul> -->
