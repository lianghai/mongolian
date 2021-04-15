import difflib
import logging
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
corpus_dir = private_repo_dir / "misc/jirimutu/mongol_corpus"

def main():

    text = "\n".join((corpus_dir / f"almas_{i:03}.txt").read_text() for i in range(1, 65))

    def normalize_text(text: str) -> str:
        for k, v in {
            "\uFEFF": "",
            "᠊": "",
            "\u202F": " \u202F",
            "᠂": " ",
            "᠃": " ",
            "᠄": " ",
            "᠁": " ",
            "«": " ",
            "»": " ",
            "︖": " ",
            "︕": " ",
            ">": " ",
            "<": " ",
            "Q": " ",
            "D": " ",
            "⟫": " ",
            "⟪": " ",
        }.items():
            text = text.replace(k, v)
        return text

    cases = Counter[str]()
    for line in normalize_text(text).splitlines():
        cases.update(line.split(" "))

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
        elif count > 100:
            string_notation = ", ".join(
                cp_to_name.get(i) or unicodedata.name(i, f"U+{ord(i):04X}") for i in case
            )
            logging.info(f" Failed case (count {count}): {string_notation}")
            for line in [*difflib.unified_diff(eac_result, utn_result, lineterm="")][3:]:
                print(indent(line, " " * 4))

    count_sum = sum(cases.values())
    logging.info(f" Passed cases: {passed}/{count_sum} = {passed / count_sum * 100} %")


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
