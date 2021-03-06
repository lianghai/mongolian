from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Optional

import yaml
from tptq.utils.script import Script

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."

utn_dir = project_dir / ".." / "utn"


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

    def __iter__(self):
        yield from chain.from_iterable(v if v else [k] for k, v in self.immediate_members.items())

    @classmethod
    def load(cls, data) -> Category:
        immediate_members = {}
        if isinstance(data, list):
            immediate_members = {validate_case(i): None for i in data}
        elif isinstance(data, dict):
            immediate_members = {k: Category.load(v) for k, v in data.items()}
        return cls(immediate_members)  # type: ignore


@dataclass
class CharacterVariant:

    character: str
    joining_form: str
    written_units: list[str]
    conditions: list[str]
    fvs: Optional[int]
    known_fvs_usage: str
    note: str
    menksoft_puas: list[int]

    @classmethod
    def load(cls, character, joining_form, data) -> CharacterVariant:
        instance = cls(
            character,
            joining_form,
            [validate_case(i) for i in data.pop("written_units")],
            [validate_case(i) for i in data.pop("conditions", [])],
            data.pop("fvs", None),
            data.pop("known_fvs_usage", ""),
            data.pop("note", ""),
            data.pop("menksoft_puas", []),
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance

    @property
    def is_definite(self) -> bool:
        return self.fvs is None and len(self.conditions) == 0

    @property
    def is_contextual(self) -> bool:
        return self.fvs is not None and len(self.conditions) > 0

    @property
    def is_manual(self) -> bool:
        return self.fvs is not None and len(self.conditions) == 0

    def __repr__(self) -> str:
        return f"""{self.character}.{"_".join(self.written_units)}.{self.joining_form}"""


@dataclass
class Character:

    cp: int
    id: str
    transcription: Optional[str] = None
    menksoft_pua: Optional[int] = None
    variants_by_joining_form: dict[str, list[CharacterVariant]] = field(default_factory=dict)
    extra_variants_by_joining_form: dict[str, list[CharacterVariant]] = field(default_factory=dict)

    @classmethod
    def load(cls, data) -> Character:
        instance = cls(
            data.pop("cp"),
            character_id := data.pop("id"),
            data.pop("transcription", None),
            data.pop("menksoft_pua", None),
            variants_by_joining_form = {
                joining_form: [
                    CharacterVariant.load(character_id, joining_form, variant_data)
                    for variant_data in v
                ] for joining_form, v in data.pop("variants_by_joining_form", {}).items()
            },
            extra_variants_by_joining_form = {
                joining_form: [
                    CharacterVariant.load(character_id, joining_form, variant_data)
                    for variant_data in v
                ] for joining_form, v in data.pop("extra_variants_by_joining_form", {}).items()
            },
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance


@dataclass
class WrittenUnit:

    id: str
    transcription: Optional[str] = None
    variant_by_joining_form: dict[str, WrittenUnitVariant] = field(default_factory=dict)

    @classmethod
    def load(cls, data) -> WrittenUnit:
        instance = cls(
            written_form_id := data.pop("id"),
            data.pop("transcription", None),
            variant_by_joining_form={
                joining_form: WrittenUnitVariant.load(written_form_id, joining_form, value)
                for joining_form, value in data.pop("variant_by_joining_form", {}).items()
            },
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance


@dataclass
class WrittenUnitVariant:

    written_unit: str
    joining_form: str
    represented_letters: list[str]
    orthogonally_joining_types: list[str]
    note: str
    typographical_decomposition: str
    menksoft_pua: int

    @classmethod
    def load(cls, written_unit, joining_form, data) -> WrittenUnitVariant:
        instance = cls(
            written_unit,
            joining_form,
            [validate_case(i if isinstance(i, str) else i["letter"]) for i in data.pop("represented_letters")],
            [validate_case(i) for i in data.pop("orthogonally_joining_types", [])],
            data.pop("note", ""),
            data.pop("typographical_decomposition", ""),
            data.pop("menksoft_pua"),
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance


class Mongolian(Script):

    code = "Mong"
    source_glyph_name_to_standard = {}

    categorization = Category.load(parse_yaml("categorization"))

    characters = dict[str, Character]()
    for data in parse_yaml("characters"):
        character = Character.load(data)
        characters[character.id] = character

    written_units = dict[str, WrittenUnit]()
    for data in parse_yaml("written-units"):
        written_unit = WrittenUnit.load(data)
        written_units[written_unit.id] = written_unit

mongolian = Mongolian()
