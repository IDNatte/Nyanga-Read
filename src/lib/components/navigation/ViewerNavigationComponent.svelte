<script lang="ts">
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';
	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';

	export let maxChapter: number | null | undefined = 0;
	export let currentChapter: number | null | undefined = 0;
</script>

<div class="h-screen fixed">
	<div class="viewer-chaptercount fixed z-50 top-5 w-full flex item-center justify-center">
		<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
			<span>{currentChapter} / {maxChapter}</span>
		</div>
	</div>

	<div class="viewer-chaptercount fixed z-50 bottom-10 w-full flex item-center justify-center">
		<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
			<ul class="viewer-navigation-button">
				<li>
					<a href="/">
						<HomeIcon />
					</a>
				</li>
				<li>
					<a href="/">
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
</div>

<style lang="postcss">
	.viewer-navigation-button {
		@apply flex divide-x divide-[#ebebeb];
	}

	.viewer-navigation-button li {
		@apply px-5 py-2;
	}
</style>
