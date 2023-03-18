<script lang="ts">
	import { goto, afterNavigate } from '$app/navigation';

	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import ChevronLeftIcon from '$lib/components/icons/ChevronLeftIcon.svelte';
	import ChevronRightIcon from '$lib/components/icons/ChevronRightIcon.svelte';
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';

	let previousPage: string = '/';
	const triggerViewerChangeNext = new Event('viewer-change:next');
	const triggerViewerChangePrev = new Event('viewer-change:prev');
	const triggerSave = new Event('manga-action:saveLocal');

	function next() {
		document.dispatchEvent(triggerViewerChangeNext);
	}

	function saveManga() {
		document.dispatchEvent(triggerSave);
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
</script>

<div>
	<div class="content">
		<slot />
	</div>

	<ViewerNavigationComponent>
		<div class="flex divide-x items-center">
			<div class="px-4">
				<a href="#!" class="flex flex-col items-center" on:click|preventDefault={saveManga}>
					<BookmarkIcon />
					<span class="font-thin text-[.8em] pt-1 capitalize">save</span>
				</a>
			</div>
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
