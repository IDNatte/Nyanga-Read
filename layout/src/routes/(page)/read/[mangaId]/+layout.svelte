<script lang="ts">
	import { goto, afterNavigate } from '$app/navigation';

	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';

	let previousPage: string = '/';

	afterNavigate(({ from }) => {
		let previous = previousPage;
		if (!from) previous = previousPage;
		if (previous?.length === 3) previousPage = from?.url.pathname || previousPage;
		if (previous?.length === 4) previousPage = '/';
	});
</script>

<div>
	<div class="content pt-2">
		<slot />
	</div>

	<div
		class="rounded-full fixed bottom-12 right-12 bg-pink-200 shadow-md px-4 py-4 flex items-center justify-center"
	>
		<a
			href="#!"
			class="flex flex-col items-center"
			on:click|preventDefault={() => goto(previousPage)}
		>
			<!-- <ReturnIcon /> -->
			<HomeIcon />
		</a>
	</div>
</div>
