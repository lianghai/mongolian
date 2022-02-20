from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).parent.parent.parent / "utn-data"

mongolian: Script


@dataclass
class Script:
    code: str
    categorization: Category
    characters: dict[str, Character]
    written_units: dict[str, WrittenUnit]


@dataclass
class Category:

    immediate_members: dict[str, None | Category]

    def __getattr__(self, name) -> Category:
        if category := self.immediate_members.get(name):
            return category
        else:
            raise AttributeError

    def __iter__(self):
        yield from chain.from_iterable(
            v if v else [k] for k, v in self.immediate_members.items()
        )

    @classmethod
    def from_data(cls, data, /) -> Category:
        immediate_members = {}
        if isinstance(data, list):
            immediate_members = {_validate_case(i): None for i in data}
        elif isinstance(data, dict):
            immediate_members = {k: Category.from_data(v) for k, v in data.items()}
        return cls(immediate_members)  # type: ignore


@dataclass
class CharacterVariant:

    character: str
    joining_form: str
    written_units: list[str]
    conditions: list[str]
    fvs: None | int
    known_fvs_usage: str
    note: str
    menksoft_puas: list[int]

    @classmethod
    def from_data(cls, character, joining_form, data) -> CharacterVariant:
        instance = cls(
            character,
            joining_form,
            [_validate_case(i) for i in data.pop("written_units")],
            [_validate_case(i) for i in data.pop("conditions", [])],
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
        return (
            f"""{self.character}.{"_".join(self.written_units)}.{self.joining_form}"""
        )


@dataclass
class Character:

    cp: int
    id: str
    transcription: None | str = None
    menksoft_pua: None | int = None
    variants_by_joining_form: dict[str, list[CharacterVariant]] = field(
        default_factory=dict
    )
    extra_variants_by_joining_form: dict[str, list[CharacterVariant]] = field(
        default_factory=dict
    )

    @classmethod
    def from_data(cls, data, /) -> Character:
        instance = cls(
            data.pop("cp"),
            character_id := data.pop("id"),
            data.pop("transcription", None),
            data.pop("menksoft_pua", None),
            variants_by_joining_form={
                joining_form: [
                    CharacterVariant.from_data(character_id, joining_form, variant_data)
                    for variant_data in v
                ]
                for joining_form, v in data.pop("variants_by_joining_form", {}).items()
            },
            extra_variants_by_joining_form={
                joining_form: [
                    CharacterVariant.from_data(character_id, joining_form, variant_data)
                    for variant_data in v
                ]
                for joining_form, v in data.pop(
                    "extra_variants_by_joining_form", {}
                ).items()
            },
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance


@dataclass
class WrittenUnit:

    id: str
    transcription: None | str = None
    variant_by_joining_form: dict[str, WrittenUnitVariant] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data, /) -> WrittenUnit:
        instance = cls(
            written_form_id := data.pop("id"),
            data.pop("transcription", None),
            variant_by_joining_form={
                joining_form: WrittenUnitVariant.from_data(
                    written_form_id, joining_form, value
                )
                for joining_form, value in data.pop(
                    "variant_by_joining_form", {}
                ).items()
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
    def from_data(cls, written_unit, joining_form, data) -> WrittenUnitVariant:
        instance = cls(
            written_unit,
            joining_form,
            [
                _validate_case(i if isinstance(i, str) else i["letter"])
                for i in data.pop("represented_letters")
            ],
            [_validate_case(i) for i in data.pop("orthogonally_joining_types", [])],
            data.pop("note", ""),
            data.pop("typographical_decomposition", ""),
            data.pop("menksoft_pua"),
        )
        if data:
            raise Exception(f"Data is not fully parsed: {data}")
        else:
            return instance


def _validate_case(case: str, /) -> str:
    literal_prefix = "."
    if case.startswith(literal_prefix):
        return case.removeprefix(literal_prefix)
    else:
        raise Exception(f""""{case}" is not a valid case literal""")


def _load_data(filename: str):
    return yaml.safe_load((DATA_DIR / filename).read_text())


mongolian = Script(
    code="Mong",
    categorization=Category.from_data(_load_data("categorization.yaml")),
    characters={
        char.id: char
        for i in _load_data("characters.yaml")
        if (char := Character.from_data(i))
    },
    written_units={
        unit.id: unit
        for i in _load_data("written-units.yaml")
        if (unit := WrittenUnit.from_data(i))
    },
)
