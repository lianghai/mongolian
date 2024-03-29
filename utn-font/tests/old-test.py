import json
from collections import Counter
from pathlib import Path

import yattag
from fontTools import unicodedata
from source import slice_joining_form
from source.data import mongolian as script

from utils import Shaper

NON_HUDUM_CODE_POINTS = "᠆᠈᠉ᡃᡄᡅᡆᡇᡈᡉᡊᡋᡌᡍᡎᡏᡐᡑᡒᡓᡔᡕᡖᡗᡘᡙᡚᡛᡜᡝᡞᡟᡠᡡᡢᡣᡤᡥᡦᡧᡨᡩᡪᡫᡬᡭᡮᡯᡰᡱᡲᡳᡴᡵᡶᡷᡸᢀᢁᢂᢃᢄᢅᢆᢇᢈᢉᢊᢋᢌᢍᢎᢏᢐᢑᢒᢓᢔᢕᢖᢗᢘᢙᢚᢛᢜᢝᢞᢟᢠᢡᢢᢣᢤᢥᢦᢧᢨᢩᢪ𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬"

FURTHER_FOLDING = str.maketrans(
    {
        0xE27E: 0xE280,
        0xE31D: 0xE280,
        0xE30C: 0xE309,
        0xE30B: 0xE310,
        0xE317: 0xE315,
        0xE320: 0xE31E,
        0xE326: 0xE322,
        0xE2B0: 0xE329,
        0xE341: 0xE33F,
        0xE344: 0xE342,
    }
)

directory = Path(__file__).parent
project_dir = directory.parent

private_repo_dir = project_dir.parent.parent / "mongolian-private"
mongoltoli_data_dir = private_repo_dir / "misc/liangjinbao/20210107/rule.mongoltoli.cn"

unknown_cps = Counter()


def main():

    # menksoft_pua_cp_ints = [*range(0xE234, 0xE497 + 1)]

    with (mongoltoli_data_dir / "xunifont_rulewords_mon.js").open() as f:
        data = "".join(["{\n"] + f.readlines()[4:-1] + ["}"])

    phonetic_pua_to_folded_mapping = make_phonetic_pua_to_folded_mapping()

    shaper = Shaper(project_dir / "DummyStateless-Regular.otf")

    case_count = 0
    failure_count = 0

    doc, tag, text = yattag.Doc().tagtext()

    cp_to_name = {
        chr(character.cp): character_id
        for character_id, character in script.characters.items()
    }

    with tag("html"):
        with tag("head"):
            doc.stag("link", rel="stylesheet", href="style.css")
        with tag("table"):
            with tag("thead"):
                with tag("tr"):
                    for content in [
                        "rule",
                        "string",
                        "expectation",
                        "graphically folded",
                        "UTN",
                        "diffing",
                    ]:
                        with tag("th"):
                            text(content)
            for rule in json.loads(data)["rulelist"]:
                rule_id = rule["ruleindex"]
                for case in rule["rulewords"]:
                    string = case["word"]
                    if any(i in NON_HUDUM_CODE_POINTS for i in string):
                        continue
                    case_count += 1
                    string_annotation = " ".join(
                        cp_to_name.get(i, f"[{i}]") for i in string
                    )
                    expectation = case["shape"]
                    graphically_folded_expectation = (
                        "".join(
                            fold_phonetic_pua(cp, phonetic_pua_to_folded_mapping)
                            for cp in expectation
                        )
                        .strip()
                        .translate(FURTHER_FOLDING)
                    )
                    utn_result = (
                        "".join(
                            convert_glyph_name_to_graphical_pua(i)
                            for i in shaper.shape_text_to_glyph_names(
                                string, features={"ss02": True}
                            )
                        )
                        .strip()
                        .translate(FURTHER_FOLDING)
                    )
                    diffing = ""
                    if graphically_folded_expectation != utn_result:
                        failure_count += 1
                        diffing = f"!{failure_count}"
                    attributes = [("class", "diff")] if diffing else []
                    with tag("tr", *attributes):
                        with tag("td"):
                            text(rule_id)
                        with tag("td"):
                            text(string)
                            doc.stag("br")
                            text(string_annotation)
                        for content in [
                            expectation,
                            graphically_folded_expectation,
                            utn_result,
                            diffing,
                        ]:
                            with tag("td"):
                                text(content)

    for cp_int, count in unknown_cps.most_common():
        print(count, f"U+{cp_int:04X}", unicodedata.name(chr(cp_int), "—"), end=", ")
    print()
    print(f"{failure_count} differences out of {case_count} test cases.")

    (directory / "old-report" / "_index.html").write_text(yattag.indent(doc.getvalue()))


def convert_glyph_name_to_graphical_pua(name: str) -> str:
    if name in ["nirugu"]:
        return ""
    elif name.startswith("pua"):
        cp = chr(int(name.removeprefix("pua"), 16))
        return cp
    else:
        if name in [
            "_" + i
            for i in [
                *script.categorization.format_control.mvs,
                *script.categorization.format_control.fvs,
            ]
        ]:
            name = name.removeprefix("_")
        if (character := script.characters.get(name)) and (
            cp_int := character.menksoft_pua
        ):
            return chr(cp_int)
        elif name in ["_nil"]:
            return ""
        else:
            return f"[{name}]"


def fold_phonetic_pua(cp: str, mapping: dict) -> str:
    cp_int = ord(cp)
    normalized_cp = None
    if cp_int in [
        0xE23A,  # MONGOLIAN TODO SOFT HYPHEN
        0xE23E,  # nirugu
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

    for character in script.characters.values():
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
                        written_unit = script.written_units[written_unit_id]
                        if written_unit_variant := written_unit.variant_by_joining_form.get(
                            written_unit_joining_form
                        ):
                            folded += chr(written_unit_variant.menksoft_pua)
                        elif written_unit_joining_form == "isol" and (
                            written_unit_variant := written_unit.variant_by_joining_form.get(
                                "init"
                            )
                        ):
                            folded += chr(written_unit_variant.menksoft_pua)
                        else:
                            raise ValueError(
                                *(f"U+{i:04X}" for i in variant.menksoft_puas),
                                written_unit.id,
                                joining_form,
                            )
                    for cp_int in variant.menksoft_puas:
                        mapping[chr(cp_int)] = folded
    return mapping


if __name__ == "__main__":
    main()
