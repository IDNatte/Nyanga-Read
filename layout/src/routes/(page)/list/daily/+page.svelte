<script lang="ts">
	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import ImageLoader from '$lib/components/image/ImageLoader.svelte';
	import { onDestroy, onMount } from 'svelte';

	let initLimit = 9
	let perPage = 3;
	let limit = 3;
	let offset = 0
	// let max = 99;

	let data: Array<any> = []
  $: data = [];

	let endObserver: HTMLDivElement;

	const observer = new IntersectionObserver(
		(event) => {
			if (event[0].intersectionRatio > 0.2) {
				limit = perPage

				if (data.length <= 9) {
					offset = limit + initLimit
				} else {
					offset = offset + perPage
				}

				getManga(offset, limit)
				console.log(`offset: ${offset} limit: ${limit}`)
			}
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: 0.2
		}
	);

  async function getInitManga() {
    let mangaData = await fetch('https://api.mangadex.org/manga?limit=9&offset=0&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art')
    if (mangaData.status === 200) {
			let manga = await mangaData.json(); 
      data = manga.data
		} else {
			throw new Error('Something went wrong :/');
		}
  }

	async function getManga(offset: number, limit: number) {
		let mangaData = await fetch(
			`https://api.mangadex.org/manga?limit=${limit}&offset=${offset}&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art`
		);

		if (mangaData.status === 200) {
			let manga = await mangaData.json();
			data = [...data, ...manga.data]
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
	<div class="loader w-full h-8 bg-pink-700 text-white flex items-center justify-center" bind:this={endObserver}>
		<span>Loading Data</span>
	</div>
</div>
