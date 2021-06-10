from __future__ import annotations

import difflib
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent

import uharfbuzz as hb
import yaml
from fontTools import unicodedata

from data import mongolian
from naming import eac_name_to_standard
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"


class Shaper:

    def __init__(self, path: Path):
        self.path = path
        face = hb.Face(path.read_bytes())  # type: ignore
        self.font = hb.Font(face)  # type: ignore
        hb.ot_font_set_funcs(self.font)  # type: ignore

    def shape_text_to_glyph_names(
        self,
        text: str,
        features: dict = None,
        gid_to_name: dict[int, str] = None,
    ) -> list[str]:

        buffer = hb.Buffer()  # type: ignore
        buffer.add_str(text)
        buffer.guess_segment_properties()

        hb.shape(self.font, buffer, features)  # type: ignore

        names = []
        for info in buffer.glyph_infos:
            gid = info.codepoint
            if gid_to_name is None:
                name = self.font.get_glyph_name(gid)
            else:
                name = gid_to_name.get(gid, f"gid{gid}")
            names.append(name)

        return names


@dataclass
class Testee:

    name: str
    shaper: Shaper
    normalizer: Callable[[list[str]], list[str]] = lambda x: x
    gid_to_name: dict[int, str] | None = None

    def shape(self, string: str) -> list[str]:
        glyph_names = self.shaper.shape_text_to_glyph_names(string, gid_to_name=self.gid_to_name)
        return self.normalizer(glyph_names)


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

    with (scripting_dir / "microsoft_tagging.yaml").open() as f:
        greg_tagging = yaml.safe_load(f)

    microsoft = Testee(
        name="microsoft",
        shaper=Shaper(private_repo_dir / "misc/gregeck/20210527/monbaiti.ttf"),
        normalizer=microsoft_normalizer,
        gid_to_name=greg_tagging | {
            1769: "nnbsp",
            241: "nirugu",
            3: "space",  # HarfBuzz pseudo space for invisible glyphs
        },
    )
    eac = Testee(
        name="eac",
        shaper=Shaper(private_repo_dir / "misc/liangjinbao/20210303/MongolQaganTig.ttf"),
        normalizer=eac_normalizer,
    )
    utn = Testee(
        name="utn",
        shaper=Shaper(project_dir / "products" / "DummyStateless-Regular.otf"),
        normalizer=utn_normalizer,
    )

    baseline_testee = microsoft
    alt_testee = eac
    corpus_tag = "jirimutu"

    filename = f"{baseline_testee.name}-vs-{alt_testee.name}-with-{corpus_tag}-corpus.txt"
    with (scripting_dir / ".." / "reports" / filename).open("w") as f:

        text = corpus_loader_by_tag[corpus_tag]()
        cases = Counter[str](
            i.group(0) for i in
            re.finditer(r"\u202F?[\u200C\u200D\u180A-\u180E\u1807\u1820-\u1842]+", text)
        )
        total = sum(cases.values())

        message = f"Total word count: {total}"
        print(message)
        print(message, file=f)

        passed = 0
        for index, (case, count) in enumerate(cases.most_common()):

            baseline = baseline_testee.shape(case)
            alt = alt_testee.shape(case)

            if baseline == alt:
                passed += count
            else:
                string_notation = ", ".join(
                    cp_to_name.get(i) or unicodedata.name(i, f"U+{ord(i):04X}") for i in case
                )
                percentage = round(count / total * 100, 4)
                if percentage >= 0.01:
                    message = f"Failed: case {index} (word count {count} ≈ {percentage} %): {string_notation}"
                    print(message)
                    print(message, file=f)
                    for line in [*difflib.unified_diff(baseline, alt, lineterm="")][3:]:
                        print(indent(line, " " * 4), file=f)
                else:
                    print(f"Failed: case {index} (word count {count} < 0.01 %): {string_notation}", file=f)

        failed = total - passed
        for message in [
            f"Failed word count: {failed}/{total} = {failed / total * 100} %",
            f"Passed word count: {passed}/{total} = {passed / total * 100} %",
        ]:
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


def microsoft_normalizer(names: list[str]) -> list[str]:
    return [
        j for i in names for j in split_ligature(i)
        if j not in {
            "space",  # HarfBuzz pseudo space for invisible glyphs
        }
    ]


def eac_normalizer(names: list[str]) -> list[str]:
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


def utn_normalizer(names: list[str]) -> list[str]:
    normalized = []
    for standard_name in names:
        if standard_name in {
            "_nil",
            "_fvs1", "_fvs2", "_fvs3", "_fvs4",
        }:
            continue
        elif standard_name == "_nnbsp":
            normalized.append("nnbsp")
        else:
            normalized.extend(split_ligature(standard_name))
    return normalized


if __name__ == "__main__":
    main()
