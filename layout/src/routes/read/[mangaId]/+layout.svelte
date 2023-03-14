<script lang="ts">
	import { goto, afterNavigate } from '$app/navigation';
	import { base } from '$app/paths';

	let previousPage: string = base;

	afterNavigate(({ from }) => {
		previousPage = from?.url.pathname || previousPage;
	});
</script>

<div>
	<div class="read-navbar">
		<a href="/">home</a>
		<a href="#!" on:click|preventDefault={() => goto(previousPage)}>back</a>
	</div>

	<div class="content">
		<slot />
	</div>
</div>

<style>
	.read-navbar {
		background-color: teal;
		position: fixed;
		display: flex;
		width: 100%;
	}

	.content {
		padding-top: 3em;
	}
</style>
