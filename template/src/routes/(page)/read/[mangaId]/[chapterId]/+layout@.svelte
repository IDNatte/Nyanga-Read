<script lang="ts">
	import type { LayoutData } from './$types';
	import { onMount } from 'svelte';
	import { goto, afterNavigate } from '$app/navigation';

	import viewerStore from '$lib/store/viewer.store';

	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';
	import ChevronLeftIcon from '$lib/components/icons/ChevronLeftIcon.svelte';
	import ChevronRightIcon from '$lib/components/icons/ChevronRightIcon.svelte';
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';
	import ViewerChapterComponent from '$lib/components/navigation/ViewerChapterComponent.svelte';

	export let data: LayoutData;

	let previousPage: string = '/';
	const triggerViewerChangeNext = new Event('viewer-change:next');
	const triggerViewerChangePrev = new Event('viewer-change:prev');
	const triggerSaveLastRead = new CustomEvent('request:set-last-read', {
		detail: {
			chapter: data.chapter,
			manga: data.manga,
			chapterName: data.chapterName,
			volumeName: data.volumeName
		}
	});

	function next() {
		document.dispatchEvent(triggerViewerChangeNext);
	}

	function prev() {
		document.dispatchEvent(triggerViewerChangePrev);
	}

	afterNavigate(({ from }) => {
		let previous = from?.url.pathname.split('/');
		if (previous?.length === 3) {
			previousPage = from?.url.pathname || previousPage;
		}
		if (previous?.length === 4) {
			previousPage = '/';
		}
	});

	onMount(() => {
		document.dispatchEvent(triggerSaveLastRead);
	});
</script>

<div>
	<ViewerChapterComponent>
		<div class="flex items-center">
			<span class="font-thin text-[.8em] capitalize"
				>Page {$viewerStore.currentPage} / {$viewerStore.totalPage}</span
			>
		</div>
	</ViewerChapterComponent>

	<div class="content">
		<slot />
	</div>

	<ViewerNavigationComponent>
		<div class="flex divide-x items-center">
			<div class="px-4">
				<a
					href="#!"
					class="flex flex-col items-center"
					on:click|preventDefault={() => goto(previousPage)}
				>
					<ReturnIcon />
					<span class="font-thin text-[.8em] pt-1 capitalize">back</span>
				</a>
			</div>

			<div class="px-4">
				<a href="#!" class="flex flex-col items-center" on:click|preventDefault={prev}>
					<ChevronLeftIcon />
					<span class="font-thin text-[.8em] pt-1 capitalize">preview</span>
				</a>
			</div>
			<div class="px-4">
				<a href="#!" class="flex flex-col items-center" on:click|preventDefault={next}>
					<ChevronRightIcon />
					<span class="font-thin text-[.8em] pt-1 capitalize">next</span>
				</a>
			</div>
		</div>
	</ViewerNavigationComponent>
</div>
