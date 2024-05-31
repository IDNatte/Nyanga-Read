<script>
	import { page } from '$app/stores';
	import { _ } from 'svelte-i18n';
</script>

<main class="error flex items-center justify-center w-full h-screen">
	<div class="flex items-center divide-x divide-slate-500">
		<div class="homepage pb-5 pt-[4.5em] flex flex-col w-full h-screen items-center justify-center">
			<span class="text-5xl pb-5">🙀</span>
			<span class="uppercase">{$_('page.errorPage.notification')}..!!</span>
			<div class="rounded bg-slate-800 w-[400px] h-[150px] mt-7 text-white flex flex-col">
				<span class="block border-b py-2 pl-2 capitalize text-sm"
					>{$_('page.errorPage.errMsg')}</span
				>
				<div class="w-full h-full flex items-center justify-center">
					<pre class="p-5">{$page.status}:{$page.error?.message}</pre>
				</div>
			</div>
		</div>
	</div>
</main>
