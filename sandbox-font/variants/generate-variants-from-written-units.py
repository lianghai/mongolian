import os, defcon, glyphConstruction
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

SPEC_DIRECTORY = "../../draft-utn/"

RULES_PATH = "./construct-variants-from-written-units.glyphConstruction"

MARK_COLOR = 0.67, 0.95, 0.38, 1

FONT_INPUT_PATH = "../components/written-units.ufo"
FONT_OUTPUT_PATH = "variants.ufo"

with open(os.path.join(SPEC_DIRECTORY, "data/phonetic-letters.txt")) as f:
    CODE_POINT_TO_LETTER_GLYPH_NAME = OrderedDict(
        line.partition("  # ")[0].split(", ")[1:] for line in f.read().splitlines()
    )

with open(os.path.join(SPEC_DIRECTORY, "data/written-units.txt")) as f:
    WRITTEN_UNIT_NAME_TO_WRITTEN_UNIT_GLYPH_NAME = OrderedDict(
        line.partition("  # ")[0].split(", ") for line in f.read().splitlines()
    )

VARIANT_DATA = OrderedDict()

with open(os.path.join(SPEC_DIRECTORY, "properties/Mongolian_Written_Forms.txt")) as f:

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

    # for line in f.read().splitlines():
    #     content, _, comment = line.partition("#")
    #     fields = [field.strip() for field in content.split(" ; ")]
    #     letter_glyph_name = CODE_POINT_TO_LETTER_GLYPH_NAME[fields[0]]
    #     if letter_glyph_name not in VARIANT_DATA:
    #         VARIANT_DATA[letter_glyph_name] = []
    #     position = fields[1]
    #     variant_parts = [
    #         WRITTEN_UNIT_NAME_TO_WRITTEN_UNIT_GLYPH_NAME[written_unit_name]
    #         for written_unit_name in fields[2].split()
    #     ]
    #     position_borrowed = fields[3]
    #     variant = position, variant_parts, position_borrowed
    #     VARIANT_DATA[letter_glyph_name].append(variant)

with open(RULES_PATH, "w") as f:

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

    # f.write("# ---\n")
    # for letter, variants in VARIANT_DATA.items():
    #     for position, parts, position_borrowed in variants:
    #         variant_position = position
    #         glyph_name = letter + "." + position + "." + "".join(parts)
    #         if position_borrowed:
    #             glyph_name += "." + position_borrowed
    #             written_form_position = position_borrowed
    #         else:
    #             written_form_position = position
    #         if len(parts) == 1:
    #             components = [parts[0] + "." + written_form_position]
    #         else:
    #             joinedness = POSITION_TO_JOINEDNESS[written_form_position]
    #             components = (
    #                 [parts[0] + "." + JOINEDNESS_TO_POSITION[(joinedness[0], 1)]]
    #                 + [part + ".medi" for part in parts[1:-1]]
    #                 + [parts[-1] + "." + JOINEDNESS_TO_POSITION[(1, joinedness[1])]]
    #             )
    #         f.write(
    #             "?" + glyph_name
    #             + " = " + " &\ ".join(components)
    #             + "\n"
    #         )
    #     f.write("# ---\n")

font = defcon.Font(FONT_INPUT_PATH)

for rule in glyphConstruction.ParseGlyphConstructionListFromString(
    source=RULES_PATH,
    font=font,  # Removing construction rules for existing glyphs.
):
    construction = glyphConstruction.GlyphConstructionBuilder(
        construction=rule,
        font=font,
    )
    if construction.name in font:
        raise ValueError(f"Duplicated construction. `{construction.name}` has already been constructed.")
    glyph = font.newGlyph(construction.name)
    glyph.clear()
    glyph.width = construction.width
    glyph.unicode = construction.unicode
    glyph.note = construction.note
    construction.draw(glyph.getPen())
    if construction.markColor:
        glyph.markColor = construction.markColor
    else:
        glyph.markColor = MARK_COLOR
    print(glyph.name)

glyphs_app_glyphOrder = font.lib["com.schriftgestaltung.glyphOrder"]
for glyph_name in font.glyphOrder:
    if glyph_name not in glyphs_app_glyphOrder:
        glyphs_app_glyphOrder.append(glyph_name)

font.save(FONT_OUTPUT_PATH)
