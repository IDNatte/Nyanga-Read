<script lang="ts">
	export let link: string | null = null;
</script>

<div class="card my-5 mx-2 shadow relative">
	{#if link !== null}
		<a href={link}>
			<slot name="card-image" />
			<div class="card-title absolute bottom-0 bg-pink-200 w-full">
				<slot name="card-title" />
			</div>
		</a>
	{:else}
		<slot name="card-image" />
		<div class="card-title absolute bottom-0 bg-pink-200 w-full">
			<slot name="card-title" />
		</div>
	{/if}
</div>
