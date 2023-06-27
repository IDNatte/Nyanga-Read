<script lang="ts">
	import type { LayoutData } from './$types';

	import { invalidateAll } from '$app/navigation';
	import { fade } from 'svelte/transition';

	import { Toaster } from 'svelte-french-toast';
	import toast from 'svelte-french-toast';
	import { find } from 'lodash';

	import refresh from '$lib/actions/page/refresh';
	import markdown from '$lib/utils/markdown';

	import loaderStore from '$lib/store/loader/loader.store';

	import ModalComponent from '$lib/components/modal/ModalComponent.svelte';
	import PageLoader from '$lib/components/loader/PageLoader.svelte';
	import TransalateIcon from '$lib/components/icons/TransalateIcon.svelte';

	export let data: LayoutData;
	console.log(data.setting);

	const language = [
		{ setting_type: 'language', value: '', title: 'Select Language' },
		{ setting_type: 'language', value: 'en', title: 'English' },
		{ setting_type: 'language', value: 'id', title: 'Bahasa Indonesia' }
	];

	const content = [
		{ setting_type: 'content', value: '', title: 'Select Content' },
		{ setting_type: 'content', value: 'safe', title: 'Safe' },
		{ setting_type: 'content', value: 'suggestive', title: 'Suggestive' },
		{ setting_type: 'content', value: 'erotica', title: 'Erotica (NSFW)' },
		{ setting_type: 'content', value: 'pornographic', title: '18+ (NSFW)' }
	];

	let selectedContent: any;
	let selectedLang: any;

	const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;

	async function updateContent() {
		let settingContext = find(data.setting.preferences, {
			setting_type: selectedContent.setting_type
		});
		console.log(settingContext.id);
		const content = await fetch('http://localhost:5000/ipc/settings', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			},
			body: JSON.stringify({ setting: settingContext.id, value: selectedContent.value })
		});

		if (content.status === 200) {
			const info = await content.json();
			if (info.status === 'unchanged') {
				toast.error(`${info.message} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'changed') {
				toast.success(`${info.message} 😸`, {
					position: 'top-right'
				});

				invalidateAll();
			}
		} else {
			toast.error('Something went error 😿', {
				position: 'top-right'
			});
		}
	}

	async function updateLanguage() {
		let settingContext = find(data.setting.preferences, {
			setting_type: selectedLang.setting_type
		});

		console.log(settingContext.id);
		const content = await fetch('http://localhost:5000/ipc/settings', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': pcsrfToken.value as string
			},
			body: JSON.stringify({ setting: settingContext.id, value: selectedLang.value })
		});

		if (content.status === 200) {
			const info = await content.json();
			if (info.status === 'unchanged') {
				toast.error(`${info.message} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'changed') {
				window.location.reload();
				invalidateAll();
			}
		} else {
			toast.error('Something went error 😿', {
				position: 'top-right'
			});
		}
	}
</script>

{#if $loaderStore === 'loading'}
	<div class="fixed z-50" out:fade={{ delay: 500 }}>
		<PageLoader />
	</div>
{/if}

<main
	use:refresh={{
		code: 'KeyK',
		control: true,
		callback: async () => {
			await invalidateAll();
		}
	}}
>
	<slot />
</main>

<div class="utils">
	<!-- Toast -->
	<Toaster />

	<!-- Settings Modal -->
	<ModalComponent modal="modal-settings" title="Settings" width="w-2/6" height="h-2/6">
		<div class="h-24 flex items-center">
			<div class="grid gap-4 grid-cols-1 w-full">
				<div class="w-full flex justify-between">
					<div class="flex items-center">
						<TransalateIcon />
						<span class="px-2">Current Demographic</span>
						<span class="capitalize font-bold">
							{find(data.setting.preferences, { setting_type: 'content' }).value}
						</span>
					</div>
					<select bind:value={selectedContent} on:change={updateContent}>
						{#each content as content}
							<option value={content}>
								{content.title}
							</option>
						{/each}
					</select>
				</div>

				<div class="w-full flex justify-between">
					<div class="flex items-center">
						<TransalateIcon />
						<span class="px-2">Current Language</span>
						<span class="capitalize font-bold">
							{find(data.setting.preferences, {
								setting_type: 'language'
							}).value}
						</span>
					</div>
					<select bind:value={selectedLang} on:change={updateLanguage}>
						{#each language as language}
							<option value={language}>
								{language.title}
							</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</ModalComponent>

	<!-- About Modal -->
	<ModalComponent modal="modal-about" title="About">
		<div class="description-wrapper p-5">
			<div class="detail w-full prose items-center max-w-full">
				{#if data.app.appInfo}
					{@html markdown(data.app.appInfo.about)}
				{/if}
			</div>
		</div>
	</ModalComponent>
</div>
