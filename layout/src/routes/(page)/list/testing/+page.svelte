<script lang="ts">
	// import type { PageData } from './$types';

	import CardComponent from '$lib/components/card/CardComponent.svelte';
	import { onDestroy, onMount } from 'svelte';

	// export let data: PageData;

	let endObserver: HTMLDivElement;

	function buildThresholdList() {
		let thresholds = [];
		let numSteps = 20;

		for (let i = 1.0; i <= numSteps; i++) {
			let ratio = i / numSteps;
			thresholds.push(ratio);
		}

		thresholds.push(0);
		return thresholds;
	}

	const observer = new IntersectionObserver(
		(event) => {
			console.log(event[0].intersectionRatio);
		},
		{
			root: null,
			rootMargin: '0px',
			threshold: buildThresholdList()
		}
	);

	onMount(() => {
		observer.observe(endObserver);
	});

	onDestroy(() => {
		observer.unobserve(endObserver);
	});
</script>

<div class="content grid grid-cols-3">
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
	<CardComponent>
		<span
			>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Sed laboriosam explicabo ex.</span
		>
	</CardComponent>
</div>
<div class="loader" bind:this={endObserver}>loading content...!!</div>
