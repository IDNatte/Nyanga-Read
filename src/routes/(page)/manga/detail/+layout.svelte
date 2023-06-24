<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { page } from '$app/stores';

	import toast from 'svelte-french-toast';

	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';

	let previewPage: string = '/';

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

<main class="detail-page">
	<slot />

	<FloatNavigationComponent homeUrl="/" backUrl={previewPage} on:bookmarkClick={bookmark} />
</main>
