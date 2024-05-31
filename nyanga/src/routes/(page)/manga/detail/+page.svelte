<script lang="ts">
	import { onDestroy, onMount } from 'svelte';

	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { fade, fly } from 'svelte/transition';

	import markdown from '$lib/utils/markdown';
	import { get as get_, truncate } from 'lodash';
	import toast from 'svelte-french-toast';
	import { _ } from 'svelte-i18n';

	import detailStore from '$lib/store/ephemeral/detail/detail.store';
	import modalStore from '$lib/store/modal/modal.store';

	import { afterNavigate } from '$app/navigation';
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import ModalComponent from '$lib/components/modal/ModalComponent.svelte';
	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';

	const language: string = document.documentElement.lang;

	let pageNumber: number;
	$: pageNumber = $detailStore.page;

	let endObserver: HTMLDivElement;
	let previewPage: string = '/';
	let error: boolean = false;
	let unbookmarked: boolean;
	let bookmarked: boolean;

	$: unbookmarked;
	$: bookmarked;

	const observer = new IntersectionObserver(
		async (event: any) => {
			if (event[0].intersectionRatio > 0.5) {
				await getNextDetail(pageNumber);
			}
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: 0.5
		}
	);

	async function getNextDetail(pageNumber: number) {
		const mangaId = $page.url.searchParams.get('manga');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const manga = await fetch(
			`http://localhost:5000/ipc/get_detail/${mangaId}?page=${pageNumber}`,
			{
				headers: {
					'Content-Type': 'application/json',
					'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
					'PCSRFWV-Token': pcsrfToken.value as string
				}
			}
		);

		if (manga.status === 200) {
			const mangaDetail = await manga.json();
			const prevMangaDetail = $detailStore.manga_data;

			if (pageNumber <= mangaDetail.max_page) {
				$detailStore.page = pageNumber + 1;
			} else {
				$detailStore.page = mangaDetail.max_page + 1;
			}

			$detailStore.manga_data = [...prevMangaDetail, ...mangaDetail.manga_data];
			$detailStore.paginated = mangaDetail.paginated;
		} else {
			error = true;
		}
	}

	async function getDetail() {
		const mangaId = $page.url.searchParams.get('manga');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;
		const manga = await fetch(`http://localhost:5000/ipc/get_detail/${mangaId}`, {
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			}
		});

		if (manga.status === 200) {
			const mangaDetail = await manga.json();

			bookmarked = mangaDetail.bookmarked;
			unbookmarked = mangaDetail.bookmarked ? false : true;

			if (pageNumber <= mangaDetail.max_page) {
				$detailStore.page = pageNumber + 1;
			} else {
				$detailStore.page = mangaDetail.max_page + 1;
			}

			$detailStore.bookmarked = mangaDetail.bookmarked;
			$detailStore.manga_data = mangaDetail.manga_data;
			$detailStore.paginated = mangaDetail.paginated;
			$detailStore.detail_data = mangaDetail.detail_data;
			$detailStore.last_read = mangaDetail.last_read;
		} else {
			detailStore.set({
				bookmarked: false,
				detail_data: null,
				last_read: null,
				manga_data: [],
				page: 1,
				paginated: false
			});

			error = true;
		}
	}

	async function bookmark() {
		const mangaId = $page.url.searchParams.get('manga');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;

		const bookmark = await fetch(`http://localhost:5000/ipc/bookmark`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			},
			body: JSON.stringify({
				mangaId: mangaId
			})
		});

		if (bookmark.status === 200) {
			const info = await bookmark.json();

			if (info.status === 'error') {
				toast.error(`${get(_)('page.detailPage.error.toastBookmarkError')} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'bookmarked') {
				unbookmarked = false;
				bookmarked = true;
				toast.success(`${get(_)('page.detailPage.notif.toastBookmarked')} 😸`, {
					position: 'top-right'
				});
			}
		} else {
			toast.error(`${get(_)('page.detailPage.error.toastBookmarkError')} 😿`, {
				position: 'top-right'
			});
		}
	}

	async function unbookmark() {
		const mangaId = $page.url.searchParams.get('manga');
		const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;

		const bookmark = await fetch(`http://localhost:5000/ipc/bookmark`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			},
			body: JSON.stringify({
				mangaId: mangaId
			})
		});

		if (bookmark.status === 200) {
			const info = await bookmark.json();

			if (info.status === 'error') {
				toast.error(`${get(_)('page.detailPage.error.toastBookmarkError')} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'unbookmarked') {
				unbookmarked = true;
				bookmarked = false;
				toast.success(`${get(_)('page.detailPage.notif.toastUnbookmarked')} 😸`, {
					position: 'top-right'
				});
			}
		} else {
			toast.error(`${get(_)('page.detailPage.error.toastBookmarkError')} 😿`, {
				position: 'top-right'
			});
		}
	}

	function openImage(modal: string) {
		modalStore.set({ modal: modal, open: true });
	}

	onMount(async () => {
		try {
			await getDetail();

			observer.observe(endObserver);
		} catch (e) {}
	});

	onDestroy(() => {
		detailStore.set({
			bookmarked: false,
			detail_data: null,
			last_read: null,
			manga_data: [],
			page: 1,
			paginated: false
		});

		try {
			observer.unobserve(endObserver);
		} catch (e) {}
	});

	afterNavigate(({ from }) => {
		if (from?.url.pathname === '/manga/read') {
			previewPage = '/';
		} else {
			previewPage = from?.url.pathname || previewPage;
		}
	});
</script>

{#if $detailStore.detail_data}
	<div>
		<div in:fade|global={{ delay: 151, duration: 200 }} class="manga-detail">
			<div class="cover-img relative">
				{#each $detailStore.detail_data.relationships as { type, attributes }}
					{#if type === 'cover_art'}
						<a
							on:click|preventDefault={() => {
								openImage('image-viewer');
							}}
							href="#!"
						>
							<ImageLoaderComponent
								src="https://uploads.mangadex.org/covers/{$detailStore.detail_data
									.id}/{attributes.fileName}"
								alt={$detailStore.detail_data.attributes.title.en ||
									$detailStore.detail_data.attributes.title.ja}
								className="object-cover w-full h-96 blur-sm hover:filter-none duration-300"
							/>
						</a>
					{/if}
				{/each}

				{#if bookmarked}
					<div
						in:fly|global={{ y: -200, duration: 200 }}
						out:fade|global={{ duration: 150 }}
						class="manga-title bg-pink-300 flex items-center absolute px-3 py-2 text-white text-sm left-3 top-7 text-center rounded-full"
					>
						<BookmarkIcon className="fill-white" />
						<span class="capitalize">{$_('page.detailPage.bookmarked')}</span>
					</div>
				{/if}

				<div
					class="manga-title bg-pink-400 inline-block absolute px-3 py-2 text-white left-3 bottom-7 text-center"
				>
					<span class="block">
						{$detailStore.detail_data.attributes.title.en ||
							get_($detailStore.detail_data.attributes.title, 'ja-ro') ||
							$detailStore.detail_data.attributes.title.ja}
					</span>
					{#each $detailStore.detail_data.attributes.altTitles as altTitle}
						{#if altTitle.ja}
							<span class="block font-jpfont">{truncate(altTitle.ja, { length: 20 })}</span>
						{/if}
					{/each}
				</div>

				{#if $detailStore.last_read}
					<div
						class="continue-reading bg-pink-300 flex absolute px-3 py-2 text-white right-3 bottom-7 text-center rounded-full"
					>
						<a
							class="text-sm capitalize"
							href="/manga/read?chapter={$detailStore.last_read
								.chapter}&chapter_number={$detailStore.last_read.chapter_number}"
						>
							{$_('page.detailPage.lastReadInfo')}
							{$detailStore.last_read.chapter_number}
						</a>
					</div>
				{/if}
			</div>
			<div class="detail-content divide-y-2">
				<div class="meta-wrapper p-5">
					<div>
						{#each $detailStore.detail_data.relationships as artist}
							{#if artist.type === 'artist'}
								<span
									class="manga-title bg-pink-400 inline-block px-2 py-1 text-white text-center text-sm capitalize"
									>{$_('page.detailPage.author')} {artist.attributes.name}</span
								>
							{/if}
						{/each}
					</div>
					<div class="pt-2">
						{#each $detailStore.detail_data.attributes.tags as { attributes }}
							<span
								class="manga-title bg-pink-300 inline-block px-2 py-1 text-white text-center rounded-full text-sm ml-1"
								>{attributes.name.en || attributes.name.ja}</span
							>
						{/each}
					</div>
				</div>
				<div class="description-wrapper p-5">
					{#if $detailStore.detail_data.attributes.description}
						<div class="detail w-full prose items-center max-w-full">
							{@html markdown(
								get_($detailStore.detail_data.attributes.description, language) ||
									get_($detailStore.detail_data.attributes.description, 'en')
							)}
						</div>
					{:else}
						<div class="detail w-full text-center">
							<span class="capitalize">{$_('page.detailPage.noDesc')} 😕</span>
						</div>
					{/if}
				</div>
				<div class="content-wrapper p-5">
					<div class="chapter-list">
						<ul class="chapter-list">
							{#if $detailStore.manga_data.length !== 0}
								{#each $detailStore.manga_data as { chapter, chapter_id, title }}
									<li>
										<a href="/manga/read?chapter={chapter_id}&chapter_number={chapter}">
											Chapter {chapter}
											{#if title}
												<i>"{title}"</i>
											{/if}
										</a>
									</li>
								{/each}
							{:else}
								<span class="italic">{$_('page.detailPage.noTl')}</span>
							{/if}
						</ul>
					</div>
				</div>
			</div>
		</div>

		<FloatNavigationComponent
			homeUrl="/"
			backUrl={previewPage}
			showBookmark={bookmarked ? false : true}
			showUnbookmark={unbookmarked ? false : true}
			on:bookmarkClick={bookmark}
			on:UnbookmarkClick={unbookmark}
		/>
	</div>

	{#if $detailStore.paginated}
		<div
			class="loader w-full h-10 bg-pink-700 text-white flex items-center justify-center"
			bind:this={endObserver}
		>
			<CirclePageLoader color="stroke-white" />
			<span class="pl-3 capitalize">{$_('page.detailPage.loader')}</span>
		</div>
	{/if}

	<ModalComponent
		modal="image-viewer"
		height="h-auto"
		width="w-[30rem]"
		title={$detailStore.detail_data.attributes.title.en ||
			$detailStore.detail_data.attributes.title.ja}
	>
		{#each $detailStore.detail_data.relationships as { type, attributes }}
			{#if type === 'cover_art'}
				<img
					class="rounded w-[30rem] h-auto"
					src="https://uploads.mangadex.org/covers/{$detailStore.detail_data
						.id}/{attributes.fileName}"
					alt={$detailStore.detail_data.attributes.title.en ||
						$detailStore.detail_data.attributes.title.ja}
				/>
			{/if}
		{/each}
	</ModalComponent>
{/if}

{#if error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">{$_('page.detailPage.error.notif')}...!</span>
	</div>

	<FloatNavigationComponent
		homeUrl="/"
		backUrl={previewPage}
		showBack={true}
		showBookmark={false}
		showUnbookmark={false}
	/>
{/if}

<style lang="postcss">
	.chapter-list li a {
		@apply w-full block border rounded px-3 my-2 py-2 shadow;
	}
</style>
