[**→ Go to repo**](https://github.com/lianghai/mongolian/tree/master/sandbox-font)

# OFL FONTLOG: Sandbox font for the Mongolian script

components/shapes.glyphs → components/written-units.ufo → variants/variants.ufo

## Glyphs

The glyph **outlines** are derived from **Noto Sans Mongolian**’s source files ([googlefonts/noto-source/src/NotoSansMongolian/ at the commit 933987e](https://github.com/googlefonts/noto-source/tree/933987e2509b9ae5192420a8296f330c25df7652/src/NotoSansMongolian)), which are [archived here](https://github.com/lianghai/mongolian/tree/master/sandbox-font/references/NotoSansMongolian) for quick reference.

Only the **subset** needed by the **Hudum** writing system is kept for now.

All glyphs are **named** according to the **analysis** of [L2/19-368 ↗](https://www.unicode.org/L2/L2019/19368-draft-utn-mongolian.pdf), Draft technical note: _Text representation and shaping specification of the Mongolian script_. The format is `<phonetic letter>.<sequence of written units>.<cursive joining position>`, for example, `a.AA.isol` for the glyph ᠠ.

In this way, the glyph set and names are largely **independent** from the ongoing discussion of **shaping rules**.
