from collections import OrderedDict

POSITION_TO_JOINEDNESS = OrderedDict([
    ("isol", (0, 0)),
    ("init", (0, 1)),
    ("medi", (1, 1)),
    ("fina", (1, 0)),
])

JOINEDNESS_TO_POSITION = OrderedDict(
    (v, k) for k, v in POSITION_TO_JOINEDNESS.items()
)

with open("../draft-utn/data/phonetic-letters.txt") as f:
    CODE_POINT_TO_LETTER_GLYPH_NAME = OrderedDict(
        line.split(", ")[1:] for line in f.read().splitlines()
    )

with open("../draft-utn/data/written-units.txt") as f:
    WRITTEN_UNIT_NAME_TO_WRITTEN_UNIT_GLYPH_NAME = OrderedDict(
        line.split(", ") for line in f.read().splitlines()
    )

VARIANT_DATA = OrderedDict()
with open("../draft-utn/data/Mongolian_Written_Forms.txt") as f:
    for line in f.read().splitlines():
        content, _, comment = line.partition("#")
        fields = [field.strip() for field in content.split(" ; ")]
        letter_glyph_name = CODE_POINT_TO_LETTER_GLYPH_NAME[fields[0]]
        if letter_glyph_name not in VARIANT_DATA:
            VARIANT_DATA[letter_glyph_name] = OrderedDict(
                (position, [])
                for position in POSITION_TO_JOINEDNESS.keys()
            )
        for position, variant_field in zip(
            POSITION_TO_JOINEDNESS.keys(),
            fields[2:],
        ):
            if variant_field:
                VARIANT_DATA[letter_glyph_name][position].append([
                    WRITTEN_UNIT_NAME_TO_WRITTEN_UNIT_GLYPH_NAME[written_unit_name]
                    for written_unit_name in variant_field.split()
                ])

with open("shaping-rules-independent/variants.glyphConstruction", "w") as f:
    f.write("# ---\n")
    for letter, positions in VARIANT_DATA.items():
        # f.write(f"?{letter} = .notdef\n")
        for position, variants in positions.items():
            # f.write(f"?{letter}.{position} = .notdef\n")
            joinedness = POSITION_TO_JOINEDNESS[position]
            for parts in variants:
                if len(parts) == 1:
                    components = [parts[0] + "." + position]
                else:
                    components = (
                        [parts[0] + "." + JOINEDNESS_TO_POSITION[(joinedness[0], 1)]]
                        + [part + ".medi" for part in parts[1:-1]]
                        + [parts[-1] + "." + JOINEDNESS_TO_POSITION[(1, joinedness[1])]]
                    )
                f.write(
                    "?" + letter + "." + position + "." + "".join(parts)
                    + " = "
                    + " &\ ".join(components)
                    + "\n"
                )
        f.write("# ---\n")
