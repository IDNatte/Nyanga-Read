<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { fade, fly } from 'svelte/transition';
	import { page } from '$app/stores';

	import toast from 'svelte-french-toast';
	import markdown from '$lib/utils/markdown';

	import ImageLoaderComponent from '$lib/components/image/ImageLoaderComponent.svelte';
	import CirclePageLoader from '$lib/components/loader/CirclePageLoader.svelte';
	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';

	let previewPage: string = '/';
	let bookmarked: boolean;
	let unbookmarked: boolean;
	$: unbookmarked;
	$: bookmarked;

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
			return {
				detail: mangaDetail.detail_data.data,
				mangaLists: mangaDetail.manga_data,
				last_read: mangaDetail.last_read,
				bookmarked: mangaDetail.bookmarked
			};
		} else {
			throw new Error('Something went wrong');
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
				toast.error(`${info.message} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'bookmarked') {
				unbookmarked = false;
				bookmarked = true;
				toast.success(`${info.message} 😸`, {
					position: 'top-right'
				});
			}
		} else {
			toast.error('Something went error 😿', {
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
				toast.error(`${info.message} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'unbookmarked') {
				unbookmarked = true;
				bookmarked = false;
				toast.success(`${info.message} 😸`, {
					position: 'top-right'
				});
			}
		} else {
			toast.error('Something went error 😿', {
				position: 'top-right'
			});
		}
	}

	afterNavigate(({ from }) => {
		if (from?.url.pathname === '/manga/read') {
			previewPage = '/';
		} else {
			previewPage = from?.url.pathname || previewPage;
		}
	});
</script>

{#await getDetail()}
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
{:then data}
	<div in:fade={{ delay: 151, duration: 200 }} class="manga-detail">
		<div class="cover-img relative">
			{#each data.detail.relationships as { type, attributes }}
				{#if type === 'cover_art'}
					<ImageLoaderComponent
						src="https://uploads.mangadex.org/covers/{data.detail.id}/{attributes.fileName}"
						alt={data.detail.attributes.title.en || data.detail.attributes.title.ja}
						className="object-cover w-full h-96 blur-sm hover:filter-none duration-300"
					/>
				{/if}
			{/each}

			{#if bookmarked}
				{#key bookmarked}
					<div
						in:fly={{ y: -200, duration: 200 }}
						out:fade={{ duration: 150 }}
						class="manga-title bg-pink-300 flex items-center absolute px-3 py-2 text-white text-sm left-3 top-7 text-center rounded-full"
					>
						<BookmarkIcon className="fill-white" />
						<span>Bookmarked</span>
					</div>
				{/key}
			{/if}

			<div
				class="manga-title bg-pink-400 inline-block absolute px-3 py-2 text-white left-3 bottom-7 text-center"
			>
				<span class="block"
					>{data.detail.attributes.title.en || data.detail.attributes.title.ja}</span
				>
				{#each data.detail.attributes.altTitles as altTitle}
					{#if altTitle.en || altTitle.ja}
						<span class="block">{altTitle.en || altTitle.ja}</span>
					{/if}
				{/each}
			</div>

			{#if data.last_read}
				<div
					class="continue-reading bg-pink-300 flex absolute px-3 py-2 text-white right-3 bottom-7 text-center rounded-full"
				>
					<a
						class="text-sm capitalize"
						href="/manga/read?chapter={data.last_read.chapter}&chapter_number={data.last_read
							.chapter_number}"
					>
						last readed chapter {data.last_read.chapter_number}
					</a>
				</div>
			{/if}
		</div>
		<div class="detail-content divide-y-2">
			<div class="meta-wrapper p-5">
				<div>
					{#each data.detail.relationships as artist}
						{#if artist.type === 'artist'}
							<span
								class="manga-title bg-pink-400 inline-block px-2 py-1 text-white text-center text-sm"
								>By {artist.attributes.name}</span
							>
						{/if}
					{/each}
				</div>
				<div class="pt-2">
					{#each data.detail.attributes.tags as { attributes }}
						<span
							class="manga-title bg-pink-300 inline-block px-2 py-1 text-white text-center rounded-full text-sm ml-1"
							>{attributes.name.en || attributes.name.ja}</span
						>
					{/each}
				</div>
			</div>
			<div class="description-wrapper p-5">
				{#if data.detail.attributes.description.en}
					<div class="detail w-full prose items-center max-w-full">
						{@html markdown(data.detail.attributes.description.en)}
					</div>
				{:else}
					<div class="detail w-full text-center">
						<span>No Description 😕</span>
					</div>
				{/if}
			</div>
			<div class="content-wrapper p-5">
				<div class="chapter-list">
					<ul class="chapter-list">
						{#each data.mangaLists as { chapter, chapter_id }}
							<li>
								<a href="/manga/read?chapter={chapter_id}&chapter_number={chapter}"
									>Chapter {chapter}</a
								>
							</li>
						{/each}
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
{:catch error}
	<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
		<span class="text-5xl pb-5">🙀</span>
		<span class="uppercase">something went wrong..!!</span>
	</div>

	<FloatNavigationComponent
		homeUrl="/"
		backUrl={previewPage}
		showBack={false}
		showBookmark={false}
		showUnbookmark={false}
	/>
{/await}

<style lang="postcss">
	.chapter-list li a {
		@apply w-full block border rounded px-3 my-2 py-2 shadow;
	}
</style>
