import json
from collections import Counter
from pathlib import Path, WindowsPath

import yattag
from fontTools import unicodedata
from tptqutils.shaping import Shaper

from data import Character
from data import Mongolian as Mong
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"
mongoltoli_data_dir = private_repo_dir / "misc/liangjinbao/20210107/rule.mongoltoli.cn"

unknown_cps = Counter()

def main():

    # menksoft_pua_cp_ints = [*range(0xE234, 0xE497 + 1)]

    with (mongoltoli_data_dir / "xunifont_rulewords_mon.js").open() as f:
        data = "".join(["{\n"] + f.readlines()[4:-1] + ["}"])

    phonetic_pua_to_folded_mapping = make_phonetic_pua_to_folded_mapping()

    shaper = Shaper(project_dir / "products" / "DummyStateless-Regular.otf")

    case_count = 0
    failure_count = 0

    doc, tag, text = yattag.Doc().tagtext()

    cp_to_name = {chr(character.cp): character_id for character_id, character in Mong.characters.items()}

    with tag("html"):
        with tag("head"):
            doc.stag("link", rel="stylesheet", href="style.css")
        with tag("table"):
            with tag("thead"):
                with tag("tr"):
                    for content in ["rule", "string", "expectation", "graphically folded", "UTN", "diffing"]:
                        with tag("th"):
                            text(content)
            for rule in json.loads(data)["rulelist"]:
                rule_id = rule["ruleindex"]
                for case in rule["rulewords"]:
                    case_count += 1
                    string = case["word"]
                    string_annotation = " ".join(
                        cp_to_name.get(i, f"[{i}]") for i in string
                    )
                    expectation = case["shape"]
                    graphically_folded_expectation = "".join(
                        fold_phonetic_pua(cp, phonetic_pua_to_folded_mapping) for cp in expectation
                    ).strip()
                    utn_result = "".join(
                        convert_glyph_name_to_graphical_pua(i)
                        for i in shaper.shape_text_to_glyph_names(string, features={"ss02": True})
                    ).strip()
                    diffing = ""
                    if graphically_folded_expectation != utn_result:
                        failure_count += 1
                        diffing = f"!{failure_count}"
                    with tag("tr"):
                        with tag("td"):
                            text(rule_id)
                        with tag("td"):
                            text(string)
                            doc.stag("br")
                            text(string_annotation)
                        for content in [expectation, graphically_folded_expectation, utn_result, diffing]:
                            with tag("td"):
                                text(content)

    for cp_int, count in unknown_cps.most_common():
        print(count, f"U+{cp_int:04X}", unicodedata.name(chr(cp_int), "—"), end=", ")
    print()
    print(f"{failure_count} differences out of {case_count} test cases.")

    (project_dir / "tests" / "index.html").write_text(yattag.indent(doc.getvalue()))


def convert_glyph_name_to_graphical_pua(name: str) -> str:
    if name in ["nirugu"]:
        return ""
    elif name.startswith("pua"):
        return chr(int(name.removeprefix("pua"), 16))
    else:
        if name in ["_" + i for i in [*Mong.categorization.format_control.mvs, *Mong.categorization.format_control.fvs]]:
            name = name.removeprefix("_")
        if (character := Mong.characters.get(name)) and (cp_int := character.menksoft_pua):
            return chr(cp_int)
        elif name in ["_nil"]:
            return ""
        else:
            return f"[{name}]"


def fold_phonetic_pua(cp: str, mapping: dict) -> str:
    cp_int = ord(cp)
    normalized_cp = None
    if cp in [
        chr(0xE23A),  # MONGOLIAN TODO SOFT HYPHEN
        chr(0xE23E),  # nirugu
    ]:
        return ""
    elif folded := mapping.get(cp):
        return folded
    else:
        if cp_int in [
            0x0020,  # space
        ]:
            normalized_cp = cp
        else:
            unknown_cps.update([cp_int])
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
