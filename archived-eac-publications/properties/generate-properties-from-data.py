import unicodedata, grapheme
from collections import OrderedDict, defaultdict

graphemes = grapheme.graphemes

class Variant:
    def __init__(
        self,
        letter_name,
        position_key,
        written_units,
        position_key_borrowed=None,
        conditions=None,
    ):
        self.letter_name = letter_name
        self.position_key = position_key
        self.written_units = written_units
        self.position_key_borrowed = position_key_borrowed
        self.conditions = {
            "context": None, # default | alt
            "mvs": None, # pre | post
            "fvs": None, # 1 | 2 | 3
        }
        if not conditions:
            self.conditions["context"] = "default"
        else:
            conditions = conditions[1:-1]
            if conditions.startswith("(") and conditions.endswith(")"):
                self.conditions["context"] = "default"
                conditions = conditions[1:-1]
            fields = conditions.split("|")
            if "context" in fields:
                self.conditions["context"] = "alt"
            if "pre-mvs" in fields:
                self.conditions["mvs"] = "pre"
            if "post-mvs" in fields:
                self.conditions["mvs"] = "post"
            if "1" in fields:
                self.conditions["fvs"] = "1"
            if "2" in fields:
                self.conditions["fvs"] = "2"
            if "3" in fields:
                self.conditions["fvs"] = "3"

with open("../data/phonetic-letters.txt") as f:
    LETTER_NAME_TO_CODE_POINT = OrderedDict(
        line.split(", ")[:2] for line in f.read().splitlines()
    )

LETTER_NAME_TO_VARIANTS = defaultdict(list)
with open("../data/variant-set.txt") as f:
    for line in f.read().splitlines():
        content, _, comment = line.partition("  # ")
        if not content:
            continue
        key, _, value = line.partition(": ")
        letter_name, _, position_key = key.partition(".")
        raw_variant_descriptions = value.split(", ")
        for raw_variant_description in raw_variant_descriptions:
            written_form, _, conditions = raw_variant_description.partition(" ")
            written_form, _, position_key_borrowed = written_form.partition(".")
            variant = Variant(
                letter_name=letter_name,
                position_key=position_key,
                written_units=list(graphemes(written_form)),
                position_key_borrowed=position_key_borrowed,
                conditions=conditions,
            )
            LETTER_NAME_TO_VARIANTS[letter_name].append(variant)

with open("./Mongolian_Written_Forms.txt", "w") as f:
    for letter_name, code_point in LETTER_NAME_TO_CODE_POINT.items():
        character_name = unicodedata.name(chr(int(code_point, 16)))
        for variant in LETTER_NAME_TO_VARIANTS[letter_name]:
            fields = [code_point]
            fields.append(variant.position_key)
            field = " ".join(variant.written_units)
            width = 5
            for character in field:
                if unicodedata.category(character) == "Mn":
                    width += 1
            fields.append(field.ljust(width))
            if variant.position_key_borrowed:
                field = variant.position_key_borrowed
            else:
                field = "    "
            fields.append(field)
            for field_key, width in [
                ("context", 7),
                ("mvs",        4),
                ("fvs",        1),
            ]:
                value = variant.conditions[field_key]
                if value:
                    field = value
                else:
                    field = ""
                fields.append(field.ljust(width))
            f.write(" ; ".join(fields) + "  # " + character_name + "\n")
