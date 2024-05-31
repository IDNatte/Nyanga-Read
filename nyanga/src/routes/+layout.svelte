<script lang="ts">
	import type { LayoutData } from './$types';

	import { invalidateAll } from '$app/navigation';
	import { get } from 'svelte/store';
	import { fade } from 'svelte/transition';

	import { find } from 'lodash';
	import toast, { Toaster } from 'svelte-french-toast';
	import { _ } from 'svelte-i18n';

	import markdown from '$lib/utils/markdown';

	import loaderStore from '$lib/store/loader/loader.store';

	import PageLoader from '$lib/components/loader/PageLoader.svelte';
	import ModalComponent from '$lib/components/modal/ModalComponent.svelte';

	import BookIcon from '$lib/components/icons/BookIcon.svelte';
	import TransalateIcon from '$lib/components/icons/TransalateIcon.svelte';

	export let data: LayoutData;
	const pcsrfToken = document.querySelector('.pycsrf') as HTMLInputElement;

	// add your language here under this command, if you wan't to change stuff, make sure you know what you're doing
	const language = [
		// <add your language here> below is example value
		// { setting_type: 'language', value: 'en', title: get(_)('app.preferences.language.langEn') },

		{ setting_type: 'language', value: 'en', title: get(_)('app.preferences.language.langEn') },
		{ setting_type: 'language', value: 'id', title: get(_)('app.preferences.language.langId') }
	];

	const content = [
		{
			setting_type: 'content',
			value: 'safe',
			title: get(_)('app.preferences.demographic.demographicSafe')
		},
		{
			setting_type: 'content',
			value: 'suggestive',
			title: get(_)('app.preferences.demographic.demographicSuggestive')
		},
		{
			setting_type: 'content',
			value: 'erotica',
			title: get(_)('app.preferences.demographic.demographicErotic')
		},
		{
			setting_type: 'content',
			value: 'pornographic',
			title: get(_)('app.preferences.demographic.demographicNSFW')
		}
	];

	let selectedContent: any = find(content, {
		value: find(data.setting.preferences, { setting_type: 'content' }).value
	});

	let selectedLang: any = find(language, {
		value: find(data.setting.preferences, { setting_type: 'language' }).value
	});

	async function updateContent() {
		let settingContext = find(data.setting.preferences, {
			setting_type: selectedContent.setting_type
		});
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
				toast.error(`${get(_)('app.saveSetting.error.notif')} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'changed') {
				toast.success(`${get(_)('app.saveSetting.saved')} 😸`, {
					position: 'top-right'
				});

				invalidateAll();
			}
		} else {
			toast.error(`${get(_)('app.saveSetting.error.notif')} 😿`, {
				position: 'top-right'
			});
		}
	}

	async function updateLanguage() {
		let settingContext = find(data.setting.preferences, {
			setting_type: selectedLang.setting_type
		});

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
				toast.error(`${get(_)('app.saveSetting.error.notif')} 😿`, {
					position: 'top-right'
				});
			}

			if (info.status === 'changed') {
				window.location.replace('/');
				invalidateAll();
			}
		} else {
			toast.error(`${get(_)('app.saveSetting.error.notif')} 😿`, {
				position: 'top-right'
			});
		}
	}
</script>

{#if $loaderStore === 'loading'}
	<div class="fixed z-50" out:fade|global={{ delay: 500 }}>
		<PageLoader />
	</div>
{/if}

<main>
	<slot />
</main>

<div class="utils">
	<!-- Toast -->
	<Toaster />

	<!-- Settings Modal -->
	<ModalComponent
		modal="modal-settings"
		title={$_('app.modal.settings')}
		width="w-3/6"
		height="h-2/6"
	>
		<div class="h-24 flex items-center">
			<div class="grid gap-4 grid-cols-1 w-full">
				<div class="w-full flex justify-between">
					<div class="flex items-center">
						<BookIcon />
						<span class="px-2 capitalize">{$_('app.preferences.demographic.demographicTitle')}</span
						>
					</div>
					<select
						class="rounded px-2 capitalize"
						bind:value={selectedContent}
						on:change={updateContent}
					>
						{#each content as content}
							<option class="capitalize" value={content}>
								{content.title}
							</option>
						{/each}
					</select>
				</div>

				<div class="w-full flex justify-between">
					<div class="flex items-center">
						<TransalateIcon />
						<span class="px-2 capitalize">{$_('app.preferences.language.langTitle')}</span>
					</div>
					<select
						class="rounded px-2 capitalize"
						bind:value={selectedLang}
						on:change={updateLanguage}
					>
						{#each language as language}
							<option class="capitalize" value={language}>
								{language.title}
							</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</ModalComponent>

	<!-- About Modal -->
	<ModalComponent modal="modal-about" title={$_('app.modal.about')}>
		<div class="description-wrapper p-5">
			<div class="detail w-full prose items-center max-w-full">
				{#if data.app.appInfo}
					{@html markdown(data.app.appInfo.about)}
				{/if}
			</div>
		</div>
	</ModalComponent>
</div>
