from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Optional, Union

import yaml

scripting_path = Path(__file__)
project_dir = scripting_path.parent

utn_dir = project_dir / ".." / ".." / "utn"


class otl:
    DEFAULT_SCRIPT_TAG = "DFLT"  # fontTools.unicodedata.OTTags.DEFAULT_SCRIPT
    DEFAULT_LANGUAGE_TAG = "dflt"
    JOINING_FORM_TAGS = ["isol", "init", "medi", "fina"]


def parse_yaml(filename: str):
    path = (utn_dir / "data" / filename).with_suffix(".yaml")
    return yaml.safe_load(path.read_text())


def validate_case(case: str, /) -> str:
    literal_prefix = "."
    if case.startswith(literal_prefix):
        return case.removeprefix(literal_prefix)
    else:
        raise Exception(f'''"{case}" is not a valid case literal''')


@dataclass
class Category:

    immediate_members: dict[str, Optional[Category]]

    def __getattr__(self, name) -> Category:
        if category := self.immediate_members.get(name):
            return category
        else:
            raise AttributeError

    def members(self) -> list[str]:
        return list(chain.from_iterable(
            v.members() if v else [k] for k, v in self.immediate_members.items()
        ))

    @classmethod
    def load(cls, data) -> Category:
        immediate_members = {}
        if isinstance(data, list):
            immediate_members = {validate_case(i): None for i in data}
        elif isinstance(data, dict):
            immediate_members = {k: Category.load(v) for k, v in data.items()}
        return cls(immediate_members)  # type: ignore


@dataclass
class Character:

    cp: int
    id: str
    transcription: Optional[str] = None
    variants_by_joining_form: Optional[dict[str, list[Character.Variant]]] = field(default_factory=dict)

    @classmethod
    def load(cls, data) -> Character:
        instance = cls(
            data.pop("cp"),
            data.pop("id"),
            data.pop("transcription", None),
            variants_by_joining_form = {
                joining_form: [Character.Variant.load(variant_data) for variant_data in v]
                for joining_form, v in d.items()
            } if (d := data.pop("variants_by_joining_form", None)) else d,
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance

    @dataclass
    class Variant:

        written_units: list[str]
        conditions: list[str]
        fvs: Optional[int]
        known_fvs_usage: str
        note: str

        @classmethod
        def load(cls, data) -> Character.Variant:
            instance = cls(
                [validate_case(i) for i in data.pop("written_units")],
                [validate_case(i) for i in data.pop("conditions", [])],
                data.pop("fvs", None),
                data.pop("known_fvs_usage", ""),
                data.pop("note", ""),
            )
            if data:
                raise Exception(f"Data is not fully parsed: {data}")
            else:
                return instance


@dataclass
class WrittenUnit:

    id: str
    transcription: Optional[str] = None
    variant_by_joining_form: dict[str, WrittenUnit.Variant] = field(default_factory=dict)

    @classmethod
    def load(cls, data) -> WrittenUnit:
        instance = cls(
            data.pop("id"),
            data.pop("transcription", None),
            variant_by_joining_form={
                joining_form: WrittenUnit.Variant.load(value)
                for joining_form, value in data.pop("variant_by_joining_form", {}).items()
            },
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance

    @dataclass
    class Variant:

        represented_letters: list[str]
        orthogonally_joining_types: list[str]
        note: str
        typographical_decomposition: str
        menksoft_pua: Optional[int]

        @classmethod
        def load(cls, data) -> WrittenUnit.Variant:
            instance = cls(
                [validate_case(i if isinstance(i, str) else i["letter"]) for i in data.pop("represented_letters")],
                [validate_case(i) for i in data.pop("orthogonally_joining_types", [])],
                data.pop("note", ""),
                data.pop("typographical_decomposition", ""),
                data.pop("menksoft_pua", None),
            )
            if data:
                raise Exception(f"Data is not fully parsed: {data}")
            else:
                return instance


categorization = Category.load(parse_yaml("categorization"))

characters = {}
for data in parse_yaml("characters"):
    character = Character.load(data)
    characters[character.id] = character

written_units = {}
for data in parse_yaml("written-units"):
    written_unit = WrittenUnit.load(data)
    written_units[written_unit.id] = written_unit
