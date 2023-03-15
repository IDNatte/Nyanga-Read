<script lang="ts">
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';
	import { get } from 'svelte/store';

	import accordionStore from '$lib/store/accordion.store';

	export let title: string;

	let accordClass: HTMLElement;
	let accordHeaderClassEvent: any;

	// debug
	onMount(() => {
		accordHeaderClassEvent = (event: Event) => {
			if (
				get(accordionStore).accordionOpen === null ||
				(get(accordionStore).accordionOpen === 'close' && get(accordionStore).accordionId === null)
			) {
				accordionStore.set({ accordionOpen: 'open', accordionId: accordClass.classList[0] });
			} else if (
				get(accordionStore).accordionOpen === 'open' &&
				get(accordionStore).accordionId === accordClass.classList[0]
			) {
				accordionStore.set({ accordionOpen: 'close', accordionId: null });
			} else if (get(accordionStore).accordionOpen === 'open') {
				accordionStore.set({ accordionOpen: 'close', accordionId: null });
			}
		};
	});
</script>

<section
	class={`accordion-${(Math.random() + 1).toString(36).substring(7)}`}
	bind:this={accordClass}
>
	<header>
		<a href="#!" on:click|preventDefault={accordHeaderClassEvent}>{title}</a>
	</header>

	{#if $accordionStore.accordionOpen === 'open' && $accordionStore.accordionId === accordClass.classList[0]}
		<div class="accordion-content" transition:slide={{ duration: 500 }}>
			<slot />
		</div>
	{/if}
</section>

<style lang="postcss">
	section {
		@apply flex flex-col;
	}

	header {
		@apply flex flex-row items-center justify-start p-2 font-bold border;
	}

	header > a {
		@apply w-full capitalize;
	}

	.accordion-content {
		@apply flex flex-col p-2 border border-solid shadow w-full;
		color: var(--text-color, theme('colors.gray.800'));
	}
</style>
