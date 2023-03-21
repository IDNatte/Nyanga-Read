<script lang="ts">
	import { onMount } from "svelte";

  const triggerLoadAllBookmark = new CustomEvent('request:manga-load-all')

  onMount(() => {
    document.dispatchEvent(triggerLoadAllBookmark)
    document.addEventListener('manga-action:load-all', (event: any) => {
      console.log(event.detail.data)
    })
  })
</script>

<span>bookmark page</span>