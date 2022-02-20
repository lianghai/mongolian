import difflib
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent

import yaml
from fontTools import unicodedata
from source import JOINING_FORM_TO_JOINEDNESS, slice_joining_form
from source.data import mongolian

from utils import Shaper

directory = Path(__file__).parent
project_dir = directory.parent

tagging_dir = project_dir / "source" / "tagging"
private_repo_dir = project_dir.parent.parent / "mongolian-private"


@dataclass
class Testee:

    name: str
    shaper: Shaper
    gid_to_name: dict[int, str] | None = None
    name_to_standard: dict[str, str] | None = None
    normalizer: Callable[[list[str]], list[str]] = lambda x: x

    def shape(self, string: str) -> list[str]:
        glyph_names = self.shaper.shape_text_to_glyph_names(
            string, gid_to_name=self.gid_to_name
        )
        if self.name_to_standard is not None:
            glyph_names = [self.name_to_standard.get(i) or i for i in glyph_names]
        glyph_names = self.normalizer(glyph_names)
        glyph_names = general_normalizer(glyph_names)
        return glyph_names


corpus_loader_by_tag = {
    "combined": (
        lambda: "\n".join(
            v() for k, v in corpus_loader_by_tag.items() if k != "combined"
        )
    ),
    "jirimutu": (
        lambda: "\n".join(
            (
                private_repo_dir / f"misc/jirimutu/mongol_corpus/almas_{i:03}.txt"
            ).read_text()
            for i in range(1, 65)
        )
    ),
    "badamsuren": (
        lambda: (private_repo_dir / "misc/badamsuren/Badamsuren.txt").read_text()
    ),
}


def main():

    microsoft = Testee(
        name="microsoft",
        shaper=Shaper(private_repo_dir / "misc/gregeck/20210527/monbaiti.ttf"),
        gid_to_name=yaml.safe_load((tagging_dir / "microsoft.yaml").read_text())
        | {
            257: "a.A_A.isol",
            262: "a.A.init",
            274: "e.A.isol",
            704: "y.I.fina",
        },
        normalizer=microsoft_normalizer,
    )
    eac = Testee(
        name="eac",
        shaper=Shaper(
            private_repo_dir / "misc/liangjinbao/20210303/MongolQaganTig.ttf"
        ),
        name_to_standard=yaml.safe_load((tagging_dir / "eac.yaml").read_text()),
        normalizer=eac_normalizer,
    )
    utn = Testee(
        name="utn",
        shaper=Shaper(project_dir / "DummyStateless-Regular.otf"),
        normalizer=utn_normalizer,
    )

    for corpus_tag in [
        "jirimutu",
        "badamsuren",
    ]:
        test(eac, utn, corpus_tag)
        for alt in [eac, utn]:
            test(microsoft, alt, corpus_tag)


def test(baseline: Testee, alt: Testee, corpus_tag: str):

    print("===")
    print(f"Shaping models: {baseline.name} vs. {alt.name}")
    print(f"Corpus: {corpus_tag}")
    print("---")

    filename = f"{baseline.name}-vs-{alt.name}-with-{corpus_tag}-corpus.txt"
    with (directory / "reports" / filename).open("w") as f:

        text = corpus_loader_by_tag[corpus_tag]()
        cases = Counter[str](
            i.group(0)
            for i in re.finditer(
                r"\u202F?[\u200C\u200D\u180A-\u180E\u1807\u1820-\u1842]+", text
            )
        )
        total = sum(cases.values())

        message = f"Total word count: {total}"
        print(message)
        print(message, file=f)

        passed = 0
        for index, (case, count) in enumerate(cases.most_common()):

            baseline_shaping = baseline.shape(case)
            alt_shaping = alt.shape(case)

            if baseline_shaping == alt_shaping:
                passed += count
            else:
                string_notation = ", ".join(
                    cp_to_name.get(i) or unicodedata.name(i, f"U+{ord(i):04X}")
                    for i in case
                )
                percentage = round(count / total * 100, 4)
                if percentage >= 0.01:
                    message = f"Failed: case {index} (word count {count} ≈ {percentage} %): {string_notation}"
                    print(message)
                    print(message, file=f)
                    for line in [
                        *difflib.unified_diff(
                            baseline_shaping, alt_shaping, lineterm=""
                        )
                    ][3:]:
                        print(indent(line, " " * 4), file=f)
                else:
                    print(
                        f"Failed: case {index} (word count {count} < 0.01 %): {string_notation}",
                        file=f,
                    )

        print("---")
        failed = total - passed
        for message in [
            f"Failed word count: {failed}/{total} = {failed / total * 100} %",
            f"Passed word count: {passed}/{total} = {passed / total * 100} %",
        ]:
            print(message)
            print(message, file=f)
        print("===")


cp_to_name = {
    chr(character.cp): character_id
    for character_id, character in mongolian.characters.items()
}


def split_ligature(name: str) -> list[str]:
    name_elements = name.split(".")
    if not len(name_elements) == 3:
        return [name]
    _, graphic, joining_form = name_elements
    graphic_parts = graphic.split("_")
    joining_forms = slice_joining_form(joining_form, len(graphic_parts))
    return [".".join(i) for i in zip(graphic_parts, joining_forms)]


def general_normalizer(names: list[str]) -> list[str]:
    names_to_drop = {
        "_invisible",
    }
    name_to_standard = {f"K2.{i}": f"K.{i}" for i in JOINING_FORM_TO_JOINEDNESS.keys()}
    confusables_to_neutralized = {
        (f"{i}.isol", f"{i}.fina"): f"{i}.isol/fina" for i in ["Aa", "I", "U"]
    } | {
        (f"{i}.init", f"{i}.medi"): f"{i}.init/medi"
        for i in [
            "I",
            "O",
            "B",
            "P",
            "G",
            "Gx",
            "T",
            "D",
            "Ch",
            "Y",
            "R",
            "W",
            "F",
            "K",
            "C",
            "Z",
            "Rh",
        ]
    }
    normalized = []
    for name in names:
        if name in names_to_drop:
            continue
        name = name_to_standard.get(name) or name
        for confusables, neutralized in confusables_to_neutralized.items():
            if name in confusables:
                normalized.append(neutralized)
                break
        else:
            normalized.append(name)
    return normalized


def microsoft_normalizer(names: list[str]) -> list[str]:
    part_to_standard = {f"Hx.{i}": f"Gh.{i}" for i in JOINING_FORM_TO_JOINEDNESS.keys()}
    normalized = []
    for name in names:
        for part in split_ligature(name):
            normalized.append(part_to_standard.get(part) or part)
    return normalized


def eac_normalizer(names: list[str]) -> list[str]:
    name_to_standard = {
        "a.Aa.fina": "a.Aa.isol",
        "e.Aa.fina": "e.Aa.isol",
    }
    normalized = []
    for name in names:
        name = name_to_standard.get(name) or name
        normalized.extend(split_ligature(name))
    return normalized


def utn_normalizer(names: list[str]) -> list[str]:
    names_to_drop = {
        "_nil",
        "_fvs1",
        "_fvs2",
        "_fvs3",
        "_fvs4",
        "_masculine",
    }
    name_to_standard = {
        "_nnbsp": "nnbsp",
    }
    normalized = []
    for name in names:
        if name in names_to_drop:
            continue
        name = name_to_standard.get(name) or name
        normalized.extend(split_ligature(name))
    return normalized


if __name__ == "__main__":
    main()
