<script lang="ts">
	import { goto, afterNavigate } from '$app/navigation';

	let previousPage: string = '/';

	afterNavigate(({ from }) => {
		let previous = from?.url.pathname.split('/')
		if (previous?.length === 3) {
			previousPage = from?.url.pathname || previousPage;
		}
		if (previous?.length === 4) {
			previousPage = '/';
		}
	});
</script>

<div>
	<div class="read-navbar">
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
		padding-top: 2em;
	}
</style>
