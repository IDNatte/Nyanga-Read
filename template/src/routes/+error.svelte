<script lang="ts">
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { _ } from 'svelte-i18n';
</script>

<div
	in:fade={{ duration: 200 }}
	class="error-page flex justify-center items-center w-full h-screen flex-col"
>
	<div class="info flex flex-col items-center pb-5">
		<span class="text-6xl pb-4">🙀</span>
		<span class="font-thin italic">{$_('error.errorPage.errorPage')}</span>
	</div>
	<div
		class="traceback-msg border bg-slate-600 text-white rounded w-[70%] h-auto flex flex-col shadow-md"
	>
		<div class="w-full border-b border-slate-500 px-5 py-2 italic font-thin capitalize">
			stacktrace
		</div>
		<div class="p-4">
			<pre>{JSON.stringify($page.error, null, 2)}</pre>
		</div>
	</div>
	<div class="help flex flex-col pt-6 items-center text-sm">
		<div class="help-info">
			<div class="first-help flex justify-center">
				<span class="text-sm capitalize">{$_('error.errorPage.firstHelp.text1')}</span>
				<span class="italic capitalize px-[3px]">{$_('error.errorPage.firstHelp.text2')}</span>
				<span>{$_('error.errorPage.firstHelp.text3')}</span>
			</div>
			<div class="second-help flex flex-col">
				<div class="section-1 flex justify-center">
					<span class="italic font-bold">{$_('error.errorPage.secondHelp.text1')}</span>
					<span class="px-[3px]">{$_('error.errorPage.secondHelp.text2')}</span>
				</div>
				<div class="section-2 flex justify-center">
					<span>{$_('error.errorPage.secondHelp.text3')}</span>
					<span class="px-[4px] italic underline">https://github.com/IDNatte/mang-redr/issues</span>
					<span>{$_('error.errorPage.secondHelp.text4')}</span>
				</div>
			</div>
			<div class="third-help flex flex-col items-center py-5">
				<span class="italic">{$_('error.errorPage.thirdHelp.text1')}</span>
				<a class="capitalize font-bold underline pt-1" href="/"
					>{$_('error.errorPage.thirdHelp.gohome')}</a
				>
			</div>
		</div>
	</div>
</div>
