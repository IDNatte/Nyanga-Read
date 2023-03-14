<script lang="ts">
	import type { PageData } from './$types';
	import { invalidateAll } from '$app/navigation';

	import { register } from 'swiper/element/bundle';

	import RefreshComponent from '$lib/components/refresh/RefreshComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';

	export let data: PageData;

	register();

	const spaceBetween = 10;

	function onSwiperProgress(event: any) {
		const [swiper, progress] = event.detail;
		console.log(progress);
	}

	function onSwiperSlideChange(event: any) {
		console.log('slide change');
	}

	async function refresh() {
		await invalidateAll();
	}
</script>

<div class="content w-full h-screen pt-8">
	<swiper-container
		slides-per-view={3}
		space-between={spaceBetween}
		centered-slides={false}
		pagination={false}
		breakpoints={{ 768: { slidesPerView: 3 } }}
		loop={true}
		mousewheel={true}
		on:progress={onSwiperProgress}
		on:slidechange={onSwiperSlideChange}
	>
		{#each data.cover as { mangaId, mangaTitle, coverUrl, mangaAltTitles }}
			<swiper-slide>
				<div class="border shadow-md rounded">
					<a href="/read/{mangaId}">
						<ImageLoader src={coverUrl} alt={mangaTitle.en} />
						<div class="title text-center text-sm p-2">
							<div class="w-full">{mangaTitle.en}</div>
							<div class="w-full">
								({#each mangaAltTitles as title}
									{#if title.ja}
										<span>{title.ja}</span>,
									{/if}
									{#if title.en}
										<span>{title.en}</span>,
									{/if}
								{/each})
							</div>
						</div>
					</a>
				</div>
			</swiper-slide>
		{/each}
	</swiper-container>

	<span
		>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ab expedita vel sapiente laudantium,
		perspiciatis atque animi, unde maxime eveniet incidunt qui commodi magni minus provident sit
		minima neque necessitatibus? Placeat!</span
	>
	<!-- <li>
		<a href="/read/{mangaId}">
			<div>
				<span>{mangaTitle.en}</span>
				({#each mangaAltTitles as title}
					{#if title.ja}
						<span>{title.ja}</span>,
					{/if}
					{#if title.en}
						<span>{title.en}</span>,
					{/if}
				{/each})
			</div>
			<ImageLoader src={coverUrl} alt={mangaTitle} />
		</a>
	</li> -->

	<!-- <ul>
		{#each data.cover as { mangaId, mangaTitle, coverUrl, mangaAltTitles }}
			<li>
				<a href="/read/{mangaId}">
					<div>
						<span>{mangaTitle.en}</span>
						({#each mangaAltTitles as title}
							{#if title.ja}
								<span>{title.ja}</span>,
							{/if}
							{#if title.en}
								<span>{title.en}</span>,
							{/if}
						{/each})
					</div>
					<ImageLoader src={coverUrl} alt={mangaTitle} />
				</a>
			</li>
		{/each}
	</ul> -->
</div>

<div>
	<div class="refresher">
		<RefreshComponent on:page-refresh={refresh} />
	</div>
</div>
