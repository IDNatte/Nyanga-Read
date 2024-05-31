<script lang="ts">
	import { onMount } from 'svelte';

	export let single: boolean = false;
	export let top: number = 0;
	export let bottom: number = 0;
	export let left: number = 0;
	export let right: number = 0;
	export let className: string = 'w-auto h-auto';

	let intersect: boolean = false;
	let container: HTMLElement;

	onMount(() => {
		if (typeof intersect !== undefined) {
			const rootMargin = `${bottom}px ${left}px ${top}px ${right}px`;

			const observer = new IntersectionObserver(
				(entries) => {
					intersect = entries[0].isIntersecting;

					if (intersect && single) {
						observer.unobserve(container);
					}
				},
				{ rootMargin }
			);

			observer.observe(container);
			return () => observer.unobserve(container);
		}

		function handler() {
			const bcr = container.getBoundingClientRect();

			intersect =
				bcr.bottom + bottom > 0 &&
				bcr.right + right > 0 &&
				bcr.top - top < window.innerHeight &&
				bcr.left - left < window.innerWidth;

			if (intersect && single) {
				window.removeEventListener('scroll', handler);
			}
		}

		window.addEventListener('scroll', handler);

		return () => window.removeEventListener('scroll', handler);
	});
</script>

<div class={className} bind:this={container}>
	<slot {intersect} />
</div>
