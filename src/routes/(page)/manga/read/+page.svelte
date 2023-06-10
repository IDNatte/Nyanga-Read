<script lang="ts">
	import { page } from '$app/stores';
	import { fade } from 'svelte/transition';

	import { find } from 'lodash';

	import imageviewerStore from '$lib/store/imageviewer/imageviewer.store';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import toast from 'svelte-french-toast';

	let image: string | null | undefined = null;
	let chapter: number | null | undefined = 1;
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
			chapter = chapterData[0].chapter_number;
			maxPage = chapterData.length;

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
				chapter = nexImage?.chapterNumber;

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
				chapter = previewImage?.chapterNumber;

				window.scrollTo({
					top: 0,
					behavior: 'smooth'
				});
			}
		}
	}

	function loadImageError(chapter: string | number | null | undefined) {
		toast.error(`cannot load image for chapter`, {
			position: 'bottom-right'
		});
	}
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
	<div in:fade={{ delay: 151, duration: 200 }}>
		<ImageLoaderComponent
			on:imageloaderror={() => loadImageError(chapter)}
			className="w-full h-auto"
			src={image}
			alt={`${chapter}`}
		/>
	</div>
{:catch error}
	<span>{error}</span>
{/await}
