<script>
	import { page } from '$app/stores';
</script>

<main class="error flex items-center justify-center w-full h-screen">
	<div class="flex items-center divide-x divide-slate-500">
		<span class="font-bold text-2xl pr-2">{$page.status}</span>
		<span class="pl-2 capitalize">
			{$page.error?.message}
		</span>
	</div>
</main>
