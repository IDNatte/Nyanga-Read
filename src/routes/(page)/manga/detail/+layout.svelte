<script lang="ts">
	import { afterNavigate } from '$app/navigation';

	import DetailNavigationComponent from '$lib/components/navigation/DetailNavigationComponent.svelte';

	let previewPage: string = '/';

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

	<DetailNavigationComponent homeUrl="/" backUrl={previewPage} />
</main>
