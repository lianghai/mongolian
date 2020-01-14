import unicodedata, zipfile, grapheme
from collections import OrderedDict, defaultdict

graphemes = grapheme.graphemes

POSITION_KEYS = ["isol", "init", "medi", "fina"]

LETTER_NAME_TO_CODE_POINT = OrderedDict()
with open("../data/phonetic-letters.txt") as f:
    for line in f.read().splitlines():
        letter_name, code_point = line.partition("  # ")[0].split(", ")[:2]
        LETTER_NAME_TO_CODE_POINT[letter_name] = code_point

class Variant:
    def __init__(
        self,
        letter_name,
        position_key,
        raw_variant_description,
    ):
        self.letter_name = letter_name
        self.position_key = position_key
        fields = raw_variant_description.split()
        written_form = fields[0]
        if len(fields) == 1:
            is_contextual = False
            fvs_assignment = False
        elif len(fields) == 2:
            prefix, fvs_assignment = fields[1]
            is_contextual = False if prefix == "!" else True
        self.written_units = list(graphemes(written_form))
        self.is_contextual = is_contextual
        self.fvs_assignment = fvs_assignment

LETTER_NAME_TO_VARIANTS = defaultdict(list)
with open("../data/variants.txt") as f:
    for line in f.read().splitlines():
        content = line.partition("#")[0].rstrip()
        if not content:
            continue
        letter_name, _, value = content.partition(" : ")
        for position_key, raw_variant_description in zip(
            POSITION_KEYS,
            value.rstrip(";").split(" ; "),
        ):
            raw_variant_description = raw_variant_description.strip()
            if not raw_variant_description:
                continue
            variant = Variant(
                letter_name,
                position_key,
                raw_variant_description,
            )
            LETTER_NAME_TO_VARIANTS[letter_name].append(variant)

with open("./MongolianVariants.txt", "w") as f:
    f.write(
        "# Format:\n"
        "#   Field 0: Unicode code point value\n"
        "#   Field 1: Assigned Mongolian Free Variation Selector (FVS)\n"
        "#   Field 2: Cursive joining position\n"
        "#   Field 3: Written units\n"
        "#   Field 4: If the variant is contextually determined\n"
    )
    f.write("\n")
    for letter_name, code_point in sorted(
        LETTER_NAME_TO_CODE_POINT.items(),
        key=lambda i: int(i[1], 16),
    ):
        character_name = unicodedata.name(chr(int(code_point, 16)))
        f.write(f"# " + character_name + "\n")
        f.write("\n")
        last_fvs_assignment = None
        for variant in sorted(
            LETTER_NAME_TO_VARIANTS[letter_name],
            key=lambda v: (
                int(v.fvs_assignment) if v.fvs_assignment else 0,
                POSITION_KEYS.index(v.position_key),
            ),
        ):
            fields = [code_point]
            if (
                last_fvs_assignment is not None
                and variant.fvs_assignment != last_fvs_assignment
            ):
                f.write("\n")
            last_fvs_assignment = variant.fvs_assignment
            fields.append(
                "FVS" + variant.fvs_assignment
                if variant.fvs_assignment
                else " " * 4
            )
            fields.append(variant.position_key)
            field = " ".join(variant.written_units)
            width = 5
            for character in field:
                if unicodedata.category(character) == "Mn":
                    width += 1
            fields.append(field.ljust(width))
            fields.append(
                "Contextual"
                if variant.is_contextual
                else " " * 10
            )
            f.write(" ; ".join(fields).strip() + "\n")
        f.write("\n")
    f.write("# EOF\n")

with zipfile.ZipFile("properties.zip", "w", compression=zipfile.ZIP_DEFLATED) as f:
    for filename in [
        "MongolianContextualCategory.txt",
        "MongolianVariants.txt",
    ]:
        f.write(filename)
