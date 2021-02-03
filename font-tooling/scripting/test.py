import json
from pathlib import Path

from fontTools import unicodedata
from tptqutils.shaping import Shaper

from data import Mongolian as Mong
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"
mongoltoli_data_dir = private_repo_dir / "misc/liangjinbao/20210107/rule.mongoltoli.cn"

unknown_cps = dict[int, None]()

def main():

    # menksoft_pua_cp_ints = [*range(0xE234, 0xE497 + 1)]

    with (mongoltoli_data_dir / "xunifont_rulewords_mon.js").open() as f:
        data = "".join(["{\n"] + f.readlines()[4:-1] + ["}"])

    phonetic_pua_to_folded_mapping = make_phonetic_pua_to_folded_mapping()

    shaper = Shaper(project_dir / "products" / "DummyStateless-Regular.otf")

    case_count = 0
    failure_count = 0

    with (scripting_dir / "output.txt").open("w") as f:
        for rule in json.loads(data)["rulelist"]:
            rule_id = rule["ruleindex"]
            for case in rule["rulewords"]:
                case_count += 1
                string = case["word"]
                expectation: str = case["shape"]
                graphically_folded_expectation = "".join(
                    fold_phonetic_pua(cp, phonetic_pua_to_folded_mapping) for cp in expectation
                )
                utn_result = "".join(
                    convert_glyph_name_to_graphical_pua(i)
                    for i in shaper.shape_text_to_glyph_names(string, features={"ss02": True})
                )
                diffing = ""
                if graphically_folded_expectation != utn_result:
                    failure_count += 1
                    diffing = f"! {failure_count}"
                print("#" + rule_id, string, expectation, graphically_folded_expectation, utn_result, diffing, sep=";", file=f)

    for cp_int in unknown_cps:
        print(f"U+{cp_int:04X}", unicodedata.name(chr(cp_int), "—"))

    print(case_count, failure_count)


def convert_glyph_name_to_graphical_pua(glyph_name: str) -> str:
    if glyph_name.startswith("pua"):
        return chr(int(glyph_name.removeprefix("pua"), 16))
    elif (character := Mong.characters.get(glyph_name)) and (cp_int := character.menksoft_pua):
        return chr(cp_int)
    elif glyph_name in ["_nil"]:
        return ""
    else:
        return f"[{glyph_name}]"


def fold_phonetic_pua(cp: str, mapping: dict) -> str:
    cp_int = ord(cp)
    normalized_cp = None
    if folded := mapping.get(cp):
        return folded
    else:
        if cp_int in [
            0x0020,  # space
        ]:
            normalized_cp = cp
        else:
            unknown_cps[cp_int] = None
    if normalized_cp is None:
        normalized_cp = f"[{cp}]"
    return normalized_cp


def make_phonetic_pua_to_folded_mapping() -> dict[str, str]:

    mapping = dict[str, str]()

    for character in Mong.characters.values():
        if cp_int := character.menksoft_pua:
            cp = folded = chr(cp_int)
            mapping[cp] = folded
        else:
            for joining_form, variants in [
                *character.variants_by_joining_form.items(),
                *character.extra_variants_by_joining_form.items(),
            ]:
                for variant in variants:
                    folded = ""
                    for written_unit_id, written_unit_joining_form in zip(
                        variant.written_units,
                        slice_joining_form(joining_form, len(variant.written_units)),
                    ):
                        written_unit = Mong.written_units[written_unit_id]
                        if written_unit_variant := written_unit.variant_by_joining_form.get(written_unit_joining_form):
                            folded += chr(written_unit_variant.menksoft_pua)
                        elif written_unit_joining_form == "isol" and (
                            written_unit_variant := written_unit.variant_by_joining_form.get("init")
                        ):
                            folded += chr(written_unit_variant.menksoft_pua)
                        else:
                            raise ValueError(*(f"U+{i:04X}" for i in variant.menksoft_puas), written_unit.id, joining_form)
                    for cp_int in variant.menksoft_puas:
                        mapping[chr(cp_int)] = folded
    return mapping


if __name__ == "__main__":
    main()
