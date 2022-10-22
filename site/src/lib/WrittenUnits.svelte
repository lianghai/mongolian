<script lang="ts">
  import { onMount } from "svelte";

  let container: HTMLElement; // with content like: Gh A
  let writtenUnits: WrittenUnit[] = [];

  onMount(() => {
    const content = container.textContent ?? "";

    writtenUnits = [...content.matchAll(/[A-Z][a-z]*/g)]
      .map((i) => i[0])
      .filter((i) => i in data);

    container.textContent = writtenUnits
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

  type WrittenUnit = string;
  type JoiningForm = "isol" | "init" | "medi" | "fina";

  // from utn-data/written-units.yaml
  const data: Record<WrittenUnit, Partial<Record<JoiningForm, string>>> = {
    A: { isol: "\ue265", init: "\ue267", medi: "\ue26c", fina: "\ue268" },
    Aa: { isol: "\ue26a" },
    I: { isol: "\ue282", init: "\ue280", medi: "\ue27e", fina: "\ue27b" },
    Ix: { isol: "\ue350" },
    O: { init: "\ue289", medi: "\ue289", fina: "\ue286" },
    Ue: { fina: "\ue297" },
    U: { isol: "\ue285", fina: "\ue285" },
    Ux: { isol: "\ue351" },
    N: { init: "\ue2b3", medi: "\ue2b7", fina: "\ue2b6" },
    B: { init: "\ue2c7", medi: "\ue2c7", fina: "\ue2c3" },
    P: { init: "\ue2cd", medi: "\ue2cd", fina: "\ue2ca" },
    H: { init: "\ue2d2", medi: "\ue2d8", fina: "\ue2d6" },
    Gh: { init: "\ue2d3", medi: "\ue2d9", fina: "\ue2d7" },
    G: { init: "\ue2df", medi: "\ue2df", fina: "\ue2e8" },
    Gx: { init: "\ue2e0", medi: "\ue2e0" },
    M: { init: "\ue2f2", medi: "\ue2f4", fina: "\ue2f3" },
    L: { init: "\ue2f8", medi: "\ue2fa", fina: "\ue2f9" },
    S: { init: "\ue2fe", medi: "\ue301", fina: "\ue2ff" },
    Sh: { init: "\ue304", medi: "\ue306", fina: "\ue305" },
    T: { init: "\ue309", medi: "\ue30c", fina: "\ue30a" },
    D: { init: "\ue310", medi: "\ue30b", fina: "\ue312" },
    Dd: { medi: "\ue314", fina: "\ue311" },
    Ch: { init: "\ue315", medi: "\ue317", fina: "\ue316" },
    J: { medi: "\ue31d", fina: "\ue31b" },
    Y: { init: "\ue31e", medi: "\ue320" },
    R: { init: "\ue322", medi: "\ue326", fina: "\ue325" },
    W: { init: "\ue329", medi: "\ue2b0", fina: "\ue2af" },
    F: { init: "\ue332", medi: "\ue332", fina: "\ue32f" },
    K2: { init: "\ue338", medi: "\ue338", fina: "\ue335" },
    K: { init: "\ue33e", medi: "\ue33e", fina: "\ue33b" },
    C: { init: "\ue33f", medi: "\ue341", fina: "\ue340" },
    Z: { init: "\ue342", medi: "\ue344", fina: "\ue343" },
    Hh: { init: "\ue345", medi: "\ue347", fina: "\ue346" },
    Rh: { init: "\ue349", medi: "\ue349", fina: "\ue34a" },
    Zr: { init: "\ue34e" },
    Cr: { init: "\ue34f" },
  };
</script>

<span bind:this={container} title={writtenUnits.join(" ")}><slot /></span>

<style>
  span {
    font-size: larger;
    font-family: "Menk Vran Tig";
  }
</style>
