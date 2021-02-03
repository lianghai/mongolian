from __future__ import annotations

import re
from functools import partial
from pathlib import Path

from fontmake.font_project import FontProject
from tptqscripttools.data import REGISTER as LegacyScriptRegister
from tptqscripttools.objects import \
    DevelopmentNaming as LegacyDevelopmentNaming
from tptqutils.otl import CodeBuilder, GlyphNotInSourceFontError
from tptqutils.script import Common
from ufoLib2.objects import Font

import stateless
from data import Mongolian

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."

glyphs_dir = project_dir / "glyphs"
source_ufo_path = glyphs_dir / "variants.ufo"

otl_dir = project_dir / "otl"
otl_path = otl_dir / "stateless" / "main.fea"

product_dir = project_dir / "products"

product_format = "otf"


# def _build():

#     ufo = Font.open(glyphs_dir / "variants.ufo")
#     ufo.info.familyName = "Sandbox"
#     ufo.info.styleName = "Regular"

#     project = FontProject()
#     output_path = project._output_path(ufo, ext=product_format, output_dir=product_dir)

#     project.run_from_ufos(
#         [ufo],
#         output=[product_format],
#         # For .save_otfs:
#         remove_overlaps=False,
#         output_path=output_path,
#         debug_feature_file=(product_dir / "debug.fea").open("w")
#     )


def main():

    builder = CodeBuilder(
        script = Mongolian,
        source_font = source_ufo_path,
        validate_glyph_availability_in_source_font = False,
        implied_script_codes = [Common.code, Mongolian.code],
    )

    for name in Mongolian.characters.keys():
        try:
            name = builder.glyph_space[name]
        except GlyphNotInSourceFontError:
            continue
        builder.shaped_glyph_names[name] = None

    additional_cmaps = ["k2"]
    for name in additional_cmaps:
        name = builder.glyph_space.__getitem__(name, validate_glyph_availability_in_source_font=False)
        builder.shaped_glyph_names[name] = None

    stateless.make_otl_code_file(builder, otl_path)

    # feaLib’s include() following somehow fails.
    inlined_otl_path = otl_dir / "stateless.fea"
    include_statement_pattern = re.compile(r"include\((.+)\);\n")
    with inlined_otl_path.open("w") as inlined_otl:
        with otl_path.open() as main_otl:
            for line in main_otl:
                if match := include_statement_pattern.fullmatch(line):
                    included_otl_path = otl_path.parent / match.group(1)
                    inlined_otl.write(included_otl_path.read_text())
                else:
                    inlined_otl.write(line)

    class LegacySimpleNaming(LegacyDevelopmentNaming):
        make_name = partial(
            LegacyDevelopmentNaming.make_name,
            implied_script_codes = [Common.code, Mongolian.code],
        )

    legacy_script = LegacyScriptRegister.script_by_code[Mongolian.code]
    legacy_script.export_otl_dummy_font(
        product_dir,
        source_ufo_path = source_ufo_path,
        naming = LegacySimpleNaming,
        feature_file_path = inlined_otl_path,
    )


if __name__ == "__main__":
    main()
