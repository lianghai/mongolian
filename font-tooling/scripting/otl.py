from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from fontTools.feaLib import ast


class CodeBuilder:
    pass


@dataclass
class Lookup:
    namespace: ClassVar[dict[str, Lookup]] = {}


@dataclass
class Block:
    name: str
    statements: list[ast.Statement]


@dataclass
class Writer:

    statements: list = []

    @contextmanager
    def File(self, path: Path):
        file = ast.FeatureFile()
        try:
            yield file
        finally:
            self.statements.append(file)

    @contextmanager
    def Lookup(self, name: str, flags):
        lookup = ast.LookupBlock(name)
        try:
            yield lookup
        finally:
            self.statements.append(lookup)


def sandbox():

    scripting_dir = Path(__file__).parent

    with Writer.File(scripting_dir / "sandbox.fea") as file:
        file
