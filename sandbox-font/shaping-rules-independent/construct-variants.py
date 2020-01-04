import defcon, glyphConstruction

RULES_PATH = "variants.glyphConstruction"
MARK_COLOR = 0.8, 1, 0.4, 1
FONT_INPUT_PATH = "../encoding-independent/written-units.ufo"
FONT_OUTPUT_PATH = "variants.ufo"

font = defcon.Font(FONT_INPUT_PATH)

for rule in glyphConstruction.ParseGlyphConstructionListFromString(
    source=RULES_PATH,
    font=font,
):
    construction = glyphConstruction.GlyphConstructionBuilder(
        construction=rule,
        font=font,
    )
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

font.save(FONT_OUTPUT_PATH)
