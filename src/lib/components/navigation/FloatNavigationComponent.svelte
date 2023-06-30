<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	import UnbookmarkIcon from '$lib/components/icons/UnbookmarkIcon.svelte';
	import BookmarkIcon from '$lib/components/icons/BookmarkIcon.svelte';
	import ReturnIcon from '$lib/components/icons/ReturnIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';

	export let showUnbookmark: boolean = false;
	export let showBookmark: boolean = true;
	export let showBack: boolean = true;
	export let backUrl: string = '/';
	export let homeUrl: string;

	let dispatch = createEventDispatcher();

	function BookmarkClick() {
		dispatch('bookmarkClick');
	}

	function UnbookmarkClick() {
		dispatch('UnbookmarkClick');
	}
</script>

<div class="detail-navigation fixed bottom-8 right-6">
	<div class="bg-pink-200 px-5 py-3 rounded-full shadow">
		<ul class="detail-navigation-btn">
			{#if showBookmark}
				<li>
					<a href="#!" on:click|preventDefault={BookmarkClick}>
						<BookmarkIcon />
					</a>
				</li>
			{/if}

			{#if showUnbookmark}
				<li>
					<a href="#!" on:click|preventDefault={UnbookmarkClick}>
						<UnbookmarkIcon />
					</a>
				</li>
			{/if}

			<li>
				<a href={homeUrl}><HomeIcon /></a>
			</li>

			{#if showBack}
				<li>
					<a href={backUrl}><ReturnIcon /></a>
				</li>
			{/if}
		</ul>
	</div>
</div>

<style lang="postcss">
	.detail-navigation-btn {
		@apply flex divide-x divide-[#ebebeb];
	}

	.detail-navigation-btn li {
		@apply px-5 py-2;
	}
</style>
