<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import FloatNavigationComponent from '$lib/components/navigation/FloatNavigationComponent.svelte';

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

	<FloatNavigationComponent homeUrl="/" backUrl={previewPage} />
</main>
