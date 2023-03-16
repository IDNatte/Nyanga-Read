<script lang="ts">
	import { goto, afterNavigate } from '$app/navigation';
	import ViewerNavigationComponent from '$lib/components/navigation/ViewerNavigationComponent.svelte';

	let previousPage: string = '/';

	afterNavigate(({ from }) => {
		let previous = from?.url.pathname.split('/');
		if (previous?.length === 3) {
			previousPage = from?.url.pathname || previousPage;
		}
		if (previous?.length === 4) {
			previousPage = '/';
		}
	});
</script>

<div>
	<div class="content">
		<slot />
	</div>

	<ViewerNavigationComponent>
		<div class="flex">
			<a class="mx-3" href="#!" on:click|preventDefault={() => goto(previousPage)}>back</a>
			<a class="mx-3" href="#!" on:click|preventDefault={() => goto(previousPage)}>back</a>
			<a class="mx-3" href="#!" on:click|preventDefault={() => goto(previousPage)}>back</a>
		</div>

	</ViewerNavigationComponent>
</div>