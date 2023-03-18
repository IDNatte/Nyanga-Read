<script lang="ts">
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import { onDestroy, onMount } from 'svelte';

	let limit = 3;
	let perPage = 3;
	let max = 99;

	// let initData: Array<any> = []
	$: newData = []
  $: data = [];

	let endObserver: HTMLDivElement;

	const observer = new IntersectionObserver(
		(event) => {
			if (event[0].intersectionRatio === 1) {
				if (limit == max) {
					limit = max;
					console.log('over limit');
				} else {
					limit = limit + perPage;
					getManga(limit)
					console.log(data)
					// console.log(`limit: ${limit} per-page: ${perPage}`);
				}
			}
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: 1
		}
	);

  async function getInitManga() {
    let mangaData = await fetch('https://api.mangadex.org/manga?limit=9&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art')
    if (mangaData.status === 200) {
			let manga = await mangaData.json(); 
      data = manga.data
		} else {
			throw new Error('Something went wrong :/');
		}
  }

	async function getManga(limit: number) {
		let mangaData = await fetch(
			`https://api.mangadex.org/manga?limit=${limit}&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art`
		);

		if (mangaData.status === 200) {
			let manga = await mangaData.json();
			let newData = manga.data
			data = [...data, ...newData]
		} else {
			throw new Error('Something went wrong :/');
		}
	}


	onMount(async () => {
    await getInitManga()
		observer.observe(endObserver);
	});


	onDestroy(() => {
		observer.unobserve(endObserver);
	});
</script>

<div>
	<div class="content grid grid-cols-3">
    {#each data as { id, attributes, relationships }}
			<CardComponent>
				<a href="/read/{id}">
					{#each relationships as rel}

						{#if rel.type === 'cover_art'}
							<ImageLoader src={`https://uploads.mangadex.org/covers/${id}/${rel.attributes.fileName}`} alt={attributes.title.en} />
						{/if}
					{/each}
					<div class="title text-center text-sm p-2">
						<div class="w-full">{attributes.title.en}</div>
						<div class="w-full">
							{#if attributes.altTitles.length > 1}
								({#each attributes.altTitles as title}
									{#if title.ja}
										<span>{title.ja}</span>
									{/if}
								{/each})
							{/if}
						</div>
					</div>
				</a>
			</CardComponent>
  	{/each}
		<!-- {#await getInitManga()}
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
			<CardComponent>
				<div class="image">
					Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae autem cum quam, pariatur
					nostrum modi. Numquam sequi impedit minus, dolores possimus error quis at, laudantium amet
					inventore voluptatibus iste consectetur.
				</div>
				<div class="title">Lorem, ipsum dolor.</div>
			</CardComponent>
		{:then data}
			{#each data.data as { id, attributes, relationships }}
        <CardComponent>
          <a href="/read/{id}">
            {#each relationships as rel}
  
              {#if rel.type === 'cover_art'}
                <ImageLoader src={`https://uploads.mangadex.org/covers/${id}/${rel.attributes.fileName}`} alt={attributes.title.en} />
              {/if}
            {/each}
            <div class="title text-center text-sm p-2">
              <div class="w-full">{attributes.title.en}</div>
              <div class="w-full">
                {#if attributes.altTitles.length > 1}
                  ({#each attributes.altTitles as title}
                    {#if title.ja}
                      <span>{title.ja}</span>
                    {/if}
                  {/each})
                {/if}
              </div>
            </div>
          </a>
        </CardComponent>
			{/each}
		{:catch}
			<span>Something went wrong</span>
		{/await} -->

    <!-- {#await getManga(limit) then data}
      {#each data.data as { id, attributes, relationships }}
        <CardComponent>
          <a href="/read/{id}">
            {#each relationships as rel}

              {#if rel.type === 'cover_art'}
                <ImageLoader src={`https://uploads.mangadex.org/covers/${id}/${rel.attributes.fileName}`} alt={attributes.title.en} />
              {/if}
            {/each}
            <div class="title text-center text-sm p-2">
              <div class="w-full">{attributes.title.en}</div>
              <div class="w-full">
                {#if attributes.altTitles.length > 1}
                  ({#each attributes.altTitles as title}
                    {#if title.ja}
                      <span>{title.ja}</span>
                    {/if}
                  {/each})
                {/if}
              </div>
            </div>
          </a>
        </CardComponent>
      {/each}
    {/await} -->
	</div>
	<div class="loader w-full h-2 bg-pink-700" bind:this={endObserver} />
</div>
