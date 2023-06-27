<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { base } from '$app/paths';
	import { onMount } from 'svelte';

	import toast from 'svelte-french-toast';
	import { find } from 'lodash';

	import imageviewerStore from '$lib/store/imageviewer/imageviewer.store';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';

	let navigationShow: boolean;
	$: navigationShow = true;

	let image: string | null | undefined = null;
	let previewPage: string = base;
	let maxPage: number;

	let currentPage: number;
	let index: number;
	$: currentPage = 0;
	$: index = 0;

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

	function prevChapter() {
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

	function nextChapter() {
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

	function loadedImage() {
		currentPage = index + 1;
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
	<div class="w-full flex items-center justify-center" in:fade={{ delay: 151, duration: 200 }}>
		<ImageLoaderComponent
			on:imageloaderror={loadImageError}
			on:viewerimgloaded={loadedImage}
			className="w-11/12 h-auto flex items-center justify-center"
			src={image}
			alt={`${index + 1}`}
		/>
	</div>

	<ViewerNavigationComponent
		on:hoverIn={hoverShowNavigation}
		on:hoverOut={hoverHideNavigation}
		on:nextArrow={nextChapter}
		on:prevArrow={prevChapter}
		chapter={Number($page.url.searchParams.get('chapter_number'))}
		showArrowNavigation={navigationShow}
		showNavigation={navigationShow}
		{currentPage}
		prevPage={previewPage}
		maxPage={maxPage + 1}
		homePage="/"
	/>
{:catch error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">something went wrong..!!</span>
	</div>
{/await}
