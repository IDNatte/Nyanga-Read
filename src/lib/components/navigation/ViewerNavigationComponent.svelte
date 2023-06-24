<script lang="ts">
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	import ChevronRightIcon from '$lib/components/icons/ChevronRightIcon.svelte';
	import ChevronLeftIcon from '$lib/components/icons/ChevronLeftIcon.svelte';
	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';

	export let maxPage: number | null | undefined = 0;
	export let currentPage: number | null | undefined = 0;
	export let showArrowNavigation: boolean = true;
	export let showNavigation: boolean = true;
	export let chapter: number = 0;
	export let homePage: string;
	export let prevPage: string;

	const dispatch = createEventDispatcher();

	function mouseInbound() {
		dispatch('hoverIn');
	}

	function mousOutBound() {
		dispatch('hoverOut');
	}

	function nextArrow() {
		dispatch('nextArrow');
	}

	function prevArrow() {
		dispatch('prevArrow');
	}
</script>

<div class="h-screen fixed">
	<div class="viewer-chaptercount fixed z-50 top-5 w-full flex item-center justify-center">
		<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
			<span>Chapter {chapter} Page {currentPage} / {maxPage}</span>
		</div>
	</div>
	{#key showNavigation}
		<div
			on:mouseenter={mouseInbound}
			on:mouseleave={mousOutBound}
			class="flex w-full fixed top-2/4 justify-between px-5 {showArrowNavigation
				? 'opacity-1'
				: 'opacity-0'}"
		>
			<a href="#!" on:click|preventDefault={prevArrow} class="arrow-navigation">
				<ChevronLeftIcon className="stroke-white" />
			</a>
			<a href="#!" on:click|preventDefault={nextArrow} class="arrow-navigation">
				<ChevronRightIcon className="stroke-white" />
			</a>
		</div>
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

	.arrow-navigation {
		@apply bg-pink-300 px-2 py-2 rounded-full;
	}
</style>
