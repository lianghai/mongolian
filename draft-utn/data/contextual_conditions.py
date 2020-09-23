from enum import Enum, auto
from typing import Optional

class Character:

    """An encoded character."""

    def init(self, code_point: int):
        self.code_point = code_point

class Letter:

    """An encoded phonetic letter."""

    def init(self, identifier: str):
        self.identifier = self.ascii_transcription = identifier
        self.condition: Optional[Condition] = None

    def follows(self, context: Character) -> bool:
        return False

class Condition(Enum):
    chachlag = auto()

def resolve_condition_for_letter(letter: Letter):
    if letter.identifier in ("a", "e") and letter.follows(Character(0x180E)):
        letter.condition = Condition.chachlag
