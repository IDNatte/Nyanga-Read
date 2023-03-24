<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import { marked } from 'marked';
	import toast, { Toaster } from 'svelte-french-toast';

	import bookmarkStore from '$lib/store/bookmark.store';
	import navigationStore from '$lib/store/navigation.store';
	import WindowFrameComponent from '$lib/components/frame/WindowFrameComponent.svelte';
	import PageLoaderComponent from '$lib/components/loader/PageLoaderComponent.svelte';
	import ModalComponent from '$lib/components/modal/ModalComponent.svelte';

	import appStore from '$lib/store/app.store';

	import '../app.css';

	const triggerAppAbout = new CustomEvent('request:app-about');
	const triggerInstallUpdate = new CustomEvent('request:app-instal-update');
	const markedOptions = {
		smartLists: true,
		smartypants: true,
		gfm: true,
		breaks: false
	};

	console.log(document.documentElement.lang);

	function installUpdate() {
		document.dispatchEvent(triggerInstallUpdate);
	}

	onMount(() => {
		document.dispatchEvent(triggerAppAbout);

		document.addEventListener('manga-action:info', (event: any) => {
			toast(event.detail.info, { icon: '😸', position: 'top-right' });
		});

		document.addEventListener('manga-action:load', (event: any) => {
			bookmarkStore.set(event.detail.data);
		});

		document.addEventListener('app-action:about', (event: any) => {
			let appInfo = JSON.parse(event.detail.data.about);
			let mdxConvert = marked.parse(appInfo, markedOptions);
			$appStore.about = mdxConvert;
			$appStore.appVersion = event.detail.data.appVersion;
		});

		document.addEventListener('app-action:update', (event: any) => {
			$appStore.update = event.detail.data;
		});
	});
</script>

<WindowFrameComponent />

{#if $navigationStore === 'loading'}
	<div out:fade={{ delay: 500 }}>
		<PageLoaderComponent />
	</div>
{/if}

<main>
	<slot />
</main>

<ModalComponent modal="about-modal" title="About Nyanga 😸">
	<div class="prose">
		{@html $appStore.about}
	</div>
</ModalComponent>

<ModalComponent modal="update-modal" title="Update Nyanga 😸">
	<div class="flex items-center justify-center flex-col">
		<div class="icon py-4 {$appStore.update?.checking ? 'animate-bounce' : ''}">
			<span class="text-9xl">😸</span>
		</div>
		<div class="app-info py-3 flex flex-col justify-center items-center">
			<span class="font-thin text-3xl capitalize">Nyanga read </span>
			<span class="py-3 text-lg capitalize">version {$appStore.appVersion}</span>
			{#if $appStore.update?.status === 'update-available'}
				<span class="py-3 text-md capitalize">New update available 😸</span>
			{/if}
			{#if $appStore.update?.status === 'update-unavailable'}
				<span class="py-3 text-md capitalize">You're @ latest version 🎉</span>
			{/if}
			{#if $appStore.update?.status === 'error'}
				<span class="py-3 text-md capitalize">Update error 😿</span>
			{/if}
			{#if $appStore.update?.status === 'downloading'}
				<span class="py-3 text-md capitalize">Downloading update 🙀</span>
			{/if}

			{#if $appStore.update?.status === 'downloaded'}
				<a href="#!" on:click|preventDefault={installUpdate}>
					<span class="py-3 text-md capitalize">Install update (?)</span>
				</a>
			{/if}
		</div>
	</div>
</ModalComponent>

<Toaster />
