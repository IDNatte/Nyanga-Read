<script lang="ts">
	import csrfStore from '$lib/store/csrf/csrf.store';
	import { get } from 'svelte/store';

	async function testingIpc() {
		let coba = await fetch('http://localhost:5000/ipc/testing', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'User-Agent': 'pywebview-client/1.0 pywebview-ui/3.0.0',
				'PCSRFWV-Token': get(csrfStore) as string
			}
		});

		let test = await coba.json();

		console.log(test);
	}
</script>

<div>
	<button on:click={testingIpc}>testing</button>
</div>
