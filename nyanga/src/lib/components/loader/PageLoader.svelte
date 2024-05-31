<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';

	import loaderStore from '$lib/store/loader/loader.store';

	const progress = tweened(0, {
		duration: 3500,
		easing: cubicOut
	});

	const unsubscribe = loaderStore.subscribe((state) => {
		if (state === 'loaded') {
			progress.set(1, { duration: 1000 });
		}
	});

	onMount(() => {
		progress.set(0.7);
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<div class="progress-bar z-40 bg-white fixed top-0 left-0 right-0 h-[0.26em]">
	<div class="progress-slider bg-pink-400" style={`--width: ${$progress * 100}%`} />
</div>

<style>
	.progress-slider {
		width: var(--width);
		height: 100%;
	}
</style>
