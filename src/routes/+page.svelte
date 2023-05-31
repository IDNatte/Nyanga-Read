<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
	console.log(data.daily);
</script>

<div class="main-content pt-20">
	<!-- main daily content -->
	<div class="grid grid-cols-3 w-full">
		{#each data.daily as { id, attributes, relationships }}
			<div class="w-full">
				{#each relationships as cover}
					{#if cover.type === 'cover_art'}
						<img
							src="https://uploads.mangadex.org/covers/{id}/{cover.attributes.fileName}"
							alt={attributes.title.en || attributes.title.ja}
						/>
					{/if}
				{/each}
				<span>{attributes.title.en || attributes.title.ja}</span>
			</div>
		{/each}
	</div>
	<div class="see-more w-full flex justify-center">
		<a class="capitalize text-pink-400/60" href="/">see more</a>
	</div>
	<!-- end main daily content -->
</div>

<div class="main-content pt-20">
	<!-- read history content -->
	<div class="grid grid-cols-3 w-full">
		{#each data.daily as { id, attributes, relationships }}
			<div class="w-full">
				{#each relationships as cover}
					{#if cover.type === 'cover_art'}
						<img
							src="https://uploads.mangadex.org/covers/{id}/{cover.attributes.fileName}"
							alt={attributes.title.en || attributes.title.ja}
						/>
					{/if}
				{/each}
				<span>{attributes.title.en || attributes.title.ja}</span>
			</div>
		{/each}
	</div>
	<div class="see-more w-full flex justify-center">
		<a class="capitalize text-pink-400/60" href="/">see more</a>
	</div>
	<!-- end read history content -->
</div>
