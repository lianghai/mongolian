<script lang="ts">
  let slot: string; // written unit transcription, eg: M A O A G Gh O L

  import { onMount } from "svelte";
  import { writtenUnitToJoiningFormToMenksoftPUA as data } from "./data";
  import type { WrittenUnit, JoiningForm } from "./data";

  let slotted: HTMLElement;
  let writtenUnits: WrittenUnit[] = [];

  onMount(() => {
    slot = slotted.textContent!;

    writtenUnits = [...slot.matchAll(/[A-Z][a-z]*/g)]
      .map((i) => i[0])
      .filter((i) => i in data);

    slotted.textContent = writtenUnits
      .map((writtenUnit, index) => {
        let joiningForm: JoiningForm = "medi";
        if (writtenUnits.length == 1) {
          joiningForm = "isol";
        } else if (index == 0) {
          joiningForm = "init";
        } else if (index == writtenUnits.length - 1) {
          joiningForm = "fina";
        }
        return data[writtenUnit][joiningForm];
      })
      .join("");
  });
</script>

<span title={writtenUnits.join(" ")} bind:this={slotted}>
  <slot />
</span>

<style>
  span {
    font-size: larger;
    font-family: "Menk Vran Tig";
  }
</style>
