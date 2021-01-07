from __future__ import annotations

import functools
import re
from pathlib import Path

from tptqscripttools.data import REGISTER
from tptqscripttools.objects import DevelopmentNaming, Script
from tptqscripttools.otl import GlyphSpace

from stateless import make_otl_file as make_stateless_otl_file

scripting_path = Path(__file__)
project_dir = scripting_path.parent / ".."

glyphs_dir = project_dir / "glyphs"
otl_dir = project_dir / "otl"
product_dir = project_dir / "products"


class SimpleNaming(DevelopmentNaming):
    make_name = functools.partial(
        DevelopmentNaming.make_name, implied_script_codes = [Script.COMMON_CODE, "Mong"],
    )


def main():

    script = REGISTER.script_by_code["Mong"]

    source_ufo_path = glyphs_dir / "variants.ufo"
    glyph_space = GlyphSpace(
        script=script,
        source_path=source_ufo_path,
        validate_glyph_availability=False,  # not checking availability in a source glyph set
        naming=SimpleNaming,
    )

    otl_path = otl_dir / "stateless" / "main.fea"
    make_stateless_otl_file(scripting_path, otl_path, glyph_space)

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

    otl_path = inlined_otl_path
    script.export_otl_dummy_font(
        product_dir,
        source_ufo_path=source_ufo_path,
        naming=glyph_space.naming,
        feature_file_path=otl_path,
    )


if __name__ == "__main__":
    main()
