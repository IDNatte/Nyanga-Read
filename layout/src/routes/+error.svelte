<script lang="ts">
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
</script>

<div
	in:fade={{ duration: 200 }}
	class="error-page flex justify-center items-center w-full h-screen flex-col"
>
	<div class="info flex flex-col items-center pb-5">
		<span class="text-6xl pb-4">🙀</span>
		<span class="font-thin italic">Opps, something wen't wrong</span>
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
				<span class="text-sm">Copy</span>
				<span class="italic capitalize px-[3px]">stacktrace</span>
				<span>and search in google</span>
			</div>
			<div class="second-help flex flex-col">
				<div class="section-1 flex justify-center">
					<span class="italic font-bold">if nothing found</span>
					<span class="px-[3px]">or the result getting complicated</span>
				</div>
				<div class="section-2 flex justify-center">
					<span>go to</span>
					<span class="px-[4px] italic underline">https://github.com/IDNatte/mang-redr/issues</span>
					<span>and tell me about it</span>
				</div>
				<!-- <a class="pl-[4px] italic" href="">tell me about it</a> -->
			</div>
			<div class="third-help flex flex-col items-center py-5">
				<span class="italic">or simply just</span>
				<a class="capitalize font-bold underline pt-1" href="/">go back to home</a>
			</div>
		</div>
	</div>
</div>
