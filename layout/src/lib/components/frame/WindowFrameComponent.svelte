<script lang="ts">
	import MinimizeIcon from '$lib/components/icons/MinimizeIcon.svelte';
	import ResizeIcon from '$lib/components/icons/ResizeIcon.svelte';
	import CloseIcon from '$lib/components/icons/CloseIcon.svelte';
  import LogoIcon from '$lib/components/icons/LogoIcon.svelte';


  const triggerWindowMinimize = new CustomEvent('request:win-minimize')
  const triggerWindowResize = new CustomEvent('request:win-resize')
  const triggerWindowClose = new CustomEvent('request:win-close')

  
  function windowMinimize() {
    document.dispatchEvent(triggerWindowMinimize)
  }
  
  function windowResize() {
    document.dispatchEvent(triggerWindowResize)
  }

  function windowClose() {
    document.dispatchEvent(triggerWindowClose)
  }

</script>

<div
	class="windowframe-components flex w-full fixed z-50 shadow bg-pink-200 justify-between items-center"
>
	<div class="window-title text-slate-800 text-sm capitalize w-5/6 flex items-center px-4 font-light">
		<span><LogoIcon width="w-[20px]" /></span>
		<span class="pl-3">Read Nyanga</span>
	</div>
	<div class="window-control flex">
		<a href="#!" on:click|preventDefault={windowMinimize}>
      <MinimizeIcon width="w-4" />
    </a>
		<a href="#!" on:click|preventDefault={windowResize}>
      <ResizeIcon width="w-4" />
    </a>
		<a href="#!" class="close" on:click|preventDefault={windowClose}><CloseIcon width="w-4" /></a>
	</div>
</div>

<style lang="postcss">
	.windowframe-components {
		user-select: none;
	}

	.window-title {
		-webkit-app-region: drag;
	}

  .window-control a {
    @apply px-4 py-[0.5rem] duration-300;
  }

  .window-control a:hover {
    @apply bg-pink-500/25 text-white;
  }
</style>
