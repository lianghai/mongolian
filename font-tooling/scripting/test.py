import json
from pathlib import Path

from fontTools import unicodedata

from data import Mongolian as Mong
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"
mongoltoli_data_dir = private_repo_dir / "misc/liangjinbao/20210107/rule.mongoltoli.cn"

menksoft_pua_cp_ints = [*range(0xE234, 0xE497 + 1)]

phonetic_pua_to_written_units = dict[int, list[tuple[str, str]]]()
for character in Mong.characters.values():
    for joining_form, variants in [
        *character.variants_by_joining_form.items(),
        *character.extra_variants_by_joining_form.items(),
    ]:
        for variant in variants:
            for pua in variant.menksoft_puas:
                written_units = variant.written_units
                phonetic_pua_to_written_units[pua] = [
                    *zip(written_units, slice_joining_form(joining_form, len(written_units)))
                ]

with (mongoltoli_data_dir / "xunifont_rulewords_mon.js").open() as f:
    data = "".join(["{\n"] + f.readlines()[4:-1] + ["}"])

with (scripting_dir / "output.txt").open("w") as f:
    unknown_cps = dict[int, None]()
    for rule in json.loads(data)["rulelist"]:
        rule_id = rule["ruleindex"]
        for test_case in rule["rulewords"]:
            string = test_case["word"]
            expectation: str = test_case["shape"]
            graphically_folded_expectation = ""
            for cp in expectation:
                cp_int = ord(cp)
                normalized_cp = None
                if written_units := phonetic_pua_to_written_units.get(cp_int):
                    normalized_cp = ""
                    for written_unit, joining_form in written_units:
                        written_unit_data = Mong.written_units[written_unit]
                        if variant := written_unit_data.variant_by_joining_form.get(joining_form):
                            normalized_cp += chr(variant.menksoft_pua)
                        elif joining_form == "isol" and (variant := written_unit_data.variant_by_joining_form.get("init")):
                            normalized_cp += chr(variant.menksoft_pua)
                        else:
                            raise ValueError(f"U+{cp_int:04X}", written_unit, joining_form)
                else:
                    if cp_int in [
                        0x0020,  # space
                        0xE23E,  # nirugu
                    ]:
                        normalized_cp = cp
                    else:
                        unknown_cps[cp_int] = None
                if normalized_cp is None:
                    normalized_cp = f"[{cp}]"
                graphically_folded_expectation += normalized_cp
            print(rule_id, string, expectation, graphically_folded_expectation, sep=";", file=f)
    for cp_int in unknown_cps:
        print(f"U+{cp_int:04X}", unicodedata.name(chr(cp_int), "—"))
