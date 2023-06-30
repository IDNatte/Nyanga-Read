<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { onMount } from 'svelte';

	import toast from 'svelte-french-toast';
	import { _ } from 'svelte-i18n';
	import { find } from 'lodash';

	import imageviewerStore from '$lib/store/imageviewer/imageviewer.store';

	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';
	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';
	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';

	let arrowNavigatonShow: boolean;
	let navigationShow: boolean;
	$: arrowNavigatonShow;
	$: navigationShow;

	let image: string | null | undefined = null;
	let previewPage: string = '/';
	let maxPage: number;

	let imageLoaded: boolean;
	let currentPage: number;
	let index: number;
	$: imageLoaded = false;
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
		toast.error(`${get(_)('page.readPage.error.toastNotif')}`, {
			position: 'bottom-right'
		});
	}

	function loadedImage() {
		imageLoaded = true;
		currentPage = index + 1;
	}

	function revealNavigation(event: MouseEvent) {
		const xThresholdLeft = 50;
		const xThresholdRight = window.innerWidth - xThresholdLeft;
		const yThresholdBottom = window.innerHeight - 100;

		if (event.clientX >= xThresholdRight || event.clientX <= xThresholdLeft) {
			arrowNavigatonShow = true;
		} else {
			arrowNavigatonShow = false;
		}

		if (event.clientY >= yThresholdBottom) {
			navigationShow = true;
		} else {
			navigationShow = false;
		}
	}

	onMount(() => {
		setTimeout(() => {
			navigationShow = false;
			arrowNavigatonShow = false;
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
	{#if !imageLoaded}
		<div class="fixed w-full" in:fade={{ duration: 200 }} out:fade={{ duration: 150 }}>
			<CirclePageLoader
				color="text-pink-700"
				style={{
					className: 'w-full h-screen flex items-center justify-center',
					w: 'w-10',
					h: 'h-10'
				}}
			/>
		</div>
	{/if}

	<div
		on:mousemove={revealNavigation}
		class="w-full flex items-center justify-center"
		in:fade={{ delay: 151, duration: 200 }}
	>
		<ImageLoaderComponent
			on:imageloaderror={loadImageError}
			on:viewerimgloaded={loadedImage}
			className="w-11/12 h-auto flex items-center justify-center"
			src={image}
			alt={`${index + 1}`}
		/>
	</div>

	<ViewerNavigationComponent
		on:nextArrow={nextChapter}
		on:prevArrow={prevChapter}
		chapter={Number($page.url.searchParams.get('chapter_number'))}
		showArrowNavigation={arrowNavigatonShow}
		showNavigation={navigationShow}
		{currentPage}
		prevPage={previewPage}
		maxPage={maxPage + 1}
		homePage="/"
	/>
{:catch error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">{$_('page.readPage.error.notif')}...!!</span>
	</div>

	<FloatNavigationComponent
		homeUrl="/"
		backUrl={previewPage}
		showBack={true}
		showBookmark={false}
		showUnbookmark={false}
	/>
{/await}
