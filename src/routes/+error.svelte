<script lang="ts">
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>{$page.error?.message}</title>
</svelte:head>

<div class="error">
	<span class="status">{$page.error?.message}</span>
</div>

<style>
	.error {
		display: flex;
		align-items: center;
		max-width: 32rem;
		margin: 0 1rem;
		--bg: white;
		--fg: #222;
		--divider: #ccc;
		background: var(--bg);
		color: var(--fg);
		font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
			Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100vh;
	}

	.status {
		font-weight: 200;
		font-size: 3rem;
		line-height: 1;
		position: relative;
		top: -0.05rem;
	}

	@media (prefers-color-scheme: dark) {
		:global(body) {
			--bg: #222;
			--fg: #ddd;
			--divider: #666;
		}
	}
</style>
