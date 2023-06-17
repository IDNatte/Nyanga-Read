<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { base } from '$app/paths';

	import { find } from 'lodash';

	import imageviewerStore from '$lib/store/imageviewer/imageviewer.store';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import toast from 'svelte-french-toast';
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';
	import { onMount } from 'svelte';

	let navigationShow: boolean;
	$: navigationShow = true;

	let image: string | null | undefined = null;
	let previewPage: string = base;
	let index: number = 0;
	let maxPage: number;

	async function readManga() {
		const chapterId = $page.url.searchParams.get('chapter');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const chapterImage = await fetch(`http://localhost:5000/ipc/read_chapter/${chapterId}`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (chapterImage.status === 200) {
			const chapterData = await chapterImage.json();
			imageviewerStore.set([...chapterData]);

			// initial data
			image = chapterData[0].url;
			index = chapterData[0].index;
			maxPage = chapterData.length - 1;

			return chapterData;
		} else {
			throw new Error('something went wrong !');
		}
	}

	function navigationShortcut(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			if (index < maxPage) {
				index = ++index;
				let nexImage = find($imageviewerStore, { index: index });
				image = nexImage?.url;

				window.scrollTo({
					top: 0,
					behavior: 'smooth'
				});
			}
		}

		if (event.key === 'ArrowLeft') {
			if (index > 0) {
				index = --index;
				let previewImage = find($imageviewerStore, { index: index });
				image = previewImage?.url;

				window.scrollTo({
					top: 0,
					behavior: 'smooth'
				});
			}
		}
	}

	function loadImageError() {
		toast.error(`cannot load image for chapter`, {
			position: 'bottom-right'
		});
	}

	function hoverHideNavigation() {
		navigationShow = false;
	}

	function hoverShowNavigation() {
		navigationShow = true;
	}

	onMount(() => {
		setTimeout(() => {
			navigationShow = false;
		}, 2500);
	});

	afterNavigate(({ from }) => {
		previewPage =
			`${from?.url.pathname}?manga=${from?.url.searchParams.get('manga')}` || previewPage;
	});
</script>

<svelte:window on:keydown={navigationShortcut} />

{#await readManga()}
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
{:then}
	<!-- {chapter} -->
	<div class="w-full flex items-center justify-center" in:fade={{ delay: 151, duration: 200 }}>
		<ImageLoaderComponent
			on:imageloaderror={() => loadImageError()}
			className="w-11/12 h-auto flex items-center justify-center"
			src={image}
			alt={`${index + 1}`}
		/>
	</div>

	<ViewerNavigationComponent
		on:hoverIn={hoverShowNavigation}
		on:hoverOut={hoverHideNavigation}
		showNavigation={navigationShow}
		prevPage={previewPage}
		homePage="/"
		currentChapter={index + 1}
		maxChapter={maxPage + 1}
	/>
{:catch error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">something went wrong..!!</span>
	</div>
{/await}
