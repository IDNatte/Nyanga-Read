<script lang="ts">
	import '../app.postcss';
</script>

<main>
	<a href="/">Home Page</a>
	<a href="/about">About Page</a>
	<div class="flex flex-col">
		<slot />
	</div>
</main>
