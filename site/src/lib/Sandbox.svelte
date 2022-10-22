<script lang="ts">
  import { onMount } from "svelte";

  let slot: HTMLElement;

  onMount(() => {
    slot.textContent = slot.textContent?.toUpperCase() ?? "";
  });
</script>

<span bind:this={slot}>
  <slot />
</span>
