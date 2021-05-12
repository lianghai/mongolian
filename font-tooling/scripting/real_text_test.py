import difflib
import re
from collections import Counter
from pathlib import Path
from textwrap import indent

from fontTools import unicodedata
from tptq.utils.shaping import Shaper

from data import mongolian
from naming import eac_name_to_standard
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"
font_dir = private_repo_dir / "misc/liangjinbao/20210303"

corpus_loader_by_tag = {
    "combined": (
        lambda: "\n".join(v() for k, v in corpus_loader_by_tag.items() if k != "combined")
    ),
    "jirimutu": (
        lambda: "\n".join(
            (private_repo_dir / f"misc/jirimutu/mongol_corpus/almas_{i:03}.txt").read_text()
            for i in range(1, 65)
        )
    ),
    "badamsuren": (
        lambda: (private_repo_dir / "misc/badamsuren/Badamsuren.txt").read_text()
    ),
}

def main():

    tag = "combined"
    text = corpus_loader_by_tag[tag]()

    cases = Counter[str](
        i.group(0) for i in
        re.finditer(r"\u202F?[\u200C\u200D\u180A-\u180E\u1807\u1820-\u1842]+", text)
    )
    total = sum(cases.values())

    with (scripting_dir / ".." / "reports" / f"{tag}.txt").open("w") as f:

        message = f"Total word count: {total}"
        print(message)
        print(message, file=f)

        passed = 0
        for case, count in cases.most_common():

            eac_shaper = Shaper(font_dir / "MongolQaganTig.ttf")
            eac_names = eac_shaper.shape_text_to_glyph_names(case)
            eac_result = normalize_eac(eac_names)

            utn_shaper = Shaper(project_dir / "products" / "DummyStateless-Regular.otf")
            utn_names = utn_shaper.shape_text_to_glyph_names(case)
            utn_result = normalize_utn(utn_names)

            if eac_result == utn_result:
                passed += count
            else:
                string_notation = ", ".join(
                    cp_to_name.get(i) or unicodedata.name(i, f"U+{ord(i):04X}") for i in case
                )
                percentage = round(count / total * 100, 4)
                if percentage >= 0.01:
                    message = f"Failed case (word count {count} ≈ {percentage} %): {string_notation}"
                    print(message)
                    print(message, file=f)
                    for line in [*difflib.unified_diff(eac_result, utn_result, lineterm="")][3:]:
                        print(indent(line, " " * 4), file=f)
                else:
                    print(f"Failed case (word count {count} < 0.01 %): {string_notation}", file=f)

        message = f"Passed cases: {passed}/{total} = {passed / total * 100} %"
        print(message)
        print(message, file=f)


cp_to_name = {chr(character.cp): character_id for character_id, character in mongolian.characters.items()}


def split_ligature(name: str) -> list[str]:
    name_elements = name.split(".")
    if not len(name_elements) == 3:
        return [name]
    _, graphic, joining_form = name_elements
    graphic_parts = graphic.split("_")
    joining_forms = slice_joining_form(joining_form, len(graphic_parts))
    return [".".join(i) for i in zip(graphic_parts, joining_forms)]


def normalize_eac(names: list[str]) -> list[str]:
    normalized = []
    for eac_name in names:
        standard_name = eac_name_to_standard.get(eac_name) or eac_name
        if standard_name in [
            "space",  # HarfBuzz swap zero-width nonspacing glyphs to /space
        ]:
            continue
        standard_name = {
            "a.Aa.fina": "a.Aa.isol",
            "e.Aa.fina": "e.Aa.isol"
        }.get(standard_name) or standard_name
        normalized.extend(split_ligature(standard_name))
    return [{"K2.init": "K.init", "K2.medi": "K.medi", "K2.fina": "K.fina"}.get(i) or i for i in normalized]


def normalize_utn(names: list[str]) -> list[str]:
    normalized = []
    for standard_name in names:
        if standard_name in ["_nil"]:
            continue
        if standard_name in ["_fvs1", "_fvs2", "_fvs3", "_fvs4"]:
            continue
        if standard_name == "_nnbsp":
            normalized.append("nnbsp")
        else:
            normalized.extend(split_ligature(standard_name))
    return normalized


if __name__ == "__main__":
    main()
