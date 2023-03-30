<script lang="ts">
	import type { PageData } from './$types';
	import { beforeNavigate } from '$app/navigation';
	import { fade } from 'svelte/transition';

	import { truncate } from 'lodash';
	import { marked } from 'marked';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import accordionStore from '$lib/store/accordion.store';

	import AccordionComponent from '$lib/components/accordion/AccordionComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import { onMount } from 'svelte';

	export let data: PageData;

	const triggerGetLastRead = new CustomEvent('request:get-last-read', {
		detail: { manga: data.mangaId }
	});

	let readLatest: boolean;
	let lastChapter: string;
	let lastChapterName: string;
	let lastVolumeName: string;
	$: readLatest = false;
	$: lastChapterName = '';
	$: lastVolumeName = '';
	$: lastChapter = '';

	const markedOptions = {
		smartLists: true,
		smartypants: true,
		gfm: true,
		breaks: false
	};

	beforeNavigate(() => {
		accordionStore.set({ accordionOpen: null, accordionId: null });
	});

	onMount(() => {
		document.dispatchEvent(triggerGetLastRead);

		document.addEventListener('manga-action:last-read', (event: any) => {
			if (event.detail) {
				if (event.detail.lastread_manga === data.mangaId) {
					lastChapter = event.detail.lastread_chapter;
					lastChapterName = event.detail.lastread_chapterName;
					lastVolumeName = event.detail.lastread_volumeName;
					readLatest = true;
				}
			}
		});
	});
</script>

<div in:fade={{ duration: 200 }}>
	<div class="cover">
		{#each data.cover as { type, attributes }}
			{#if type === 'cover_art'}
				<div class="w-full h-auto relative block">
					<div class="blur-sm hover:filter-none duration-300">
						<ImageLoader
							className="h-[300px] object-cover w-full"
							src={`https://uploads.mangadex.org/covers/${data.mangaId}/${attributes.fileName}`}
							alt={data.mangaId}
						/>
					</div>
					<div>
						<span class="costume-title">{truncate(data.title, { length: 30 })}</span>
						{#if readLatest}
							<a
								class="costume-last-readed"
								href="/read/{data.mangaId}/{lastChapter}?chapter={lastChapter}&manga={data.mangaId}&chapterName={lastChapter}&volumeName={lastVolumeName}"
								>Read Vol. {lastVolumeName} Chap. {lastChapterName}
							</a>
						{/if}
					</div>
				</div>
			{/if}
		{/each}
	</div>

	{#if data.description}
		<div class="description pt-8 pb-4 w-full px-5 prose flex">
			<span class="border-l-[2px] border-pink-400 block pl-3 italic font-thin">
				{@html marked(data.description, markedOptions)}
			</span>
		</div>
	{/if}

	<div class="volume py-5">
		{#each data.volume as { volume, chapter }}
			<CardComponent>
				<AccordionComponent title={`volume ${volume}`}>
					<ul class="divide-y">
						{#each chapter as { chapterId, chapterName }}
							<li class="py-2 block">
								<a
									class="px-4 w-full block"
									href="/read/{data.mangaId}/{chapterId}?chapter={chapterId}&manga={data.mangaId}&chapterName={chapterName}&volumeName={volume}"
									>Chapter {chapterName}</a
								>
							</li>
						{/each}
					</ul>
				</AccordionComponent>
			</CardComponent>
		{/each}
	</div>
</div>

<style lang="postcss">
	.costume-last-readed {
		@apply absolute bottom-3 left-2 text-[#ffffff] bg-pink-300 px-5 py-[1.5px] rounded-full font-thin;
		text-shadow: theme('colors.pink.700') 0px 0px 5px;
		-webkit-font-smoothing: antialiased;
	}

	.costume-title {
		@apply absolute top-3 left-2 text-[#ffffff] bg-pink-300 px-5 py-[1.5px] rounded-full font-thin;
		text-shadow: theme('colors.pink.700') 0px 0px 5px;
		-webkit-font-smoothing: antialiased;
	}
</style>
