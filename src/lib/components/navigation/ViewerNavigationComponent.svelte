<script lang="ts">
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';

	export let maxChapter: number | null | undefined = 0;
	export let currentChapter: number | null | undefined = 0;
	export let showNavigation: boolean = true;
	export let homePage: string;
	export let prevPage: string;

	const dispatch = createEventDispatcher();

	function mouseInbound() {
		dispatch('hoverIn');
	}

	function mousOutBound() {
		dispatch('hoverOut');
	}
</script>

<div class="h-screen fixed">
	<div class="viewer-chaptercount fixed z-50 top-5 w-full flex item-center justify-center">
		<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
			<span>{currentChapter} / {maxChapter}</span>
		</div>
	</div>
	{#key showNavigation}
		<div
			on:mouseenter={mouseInbound}
			on:mouseleave={mousOutBound}
			transition:fade={{ duration: 100 }}
			class="viewer-chaptercount fixed z-50 bottom-10 w-full flex item-center justify-center {showNavigation
				? 'opacity-1'
				: 'opacity-0'}"
		>
			<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
				<ul class="viewer-navigation-button">
					<li>
						<a href={homePage}>
							<HomeIcon />
						</a>
					</li>
					<li>
						<a href={prevPage}>
							<ReturnIcon />
						</a>
					</li>
					<li>
						<a href="/">
							<BookmarkIcon />
						</a>
					</li>
				</ul>
			</div>
		</div>
	{/key}
</div>

<style lang="postcss">
	.viewer-navigation-button {
		@apply flex divide-x divide-[#ebebeb];
	}

	.viewer-navigation-button li {
		@apply px-5 py-2;
	}
</style>
