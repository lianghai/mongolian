import re
from pathlib import Path

from fontmake.font_project import FontProject

# from tptq.utils.glyph_set import SourceGlyphSet
# from tptq.utils.otl import GlyphNotInSourceFontError
# from tptq.utils.script import Common
# from tptqscripttools.data import REGISTER as LegacyScriptRegister
# from tptqscripttools.objects import DevelopmentNaming as LegacyDevelopmentNaming
# from tptqscripttools.objects import GlyphIdentity
from ufoLib2 import Font

# from sources import data, otl

directory = Path(__file__).parent

otl_dir = directory / "otl"
otl_path = otl_dir / "stateless" / "main.fea"


def main():

    ufo = Font()
    ufo.info.familyName = "Draft UTN"
    for glyph in Font.open(directory / "sources" / "variants.ufo"):
        ufo.addGlyph(glyph)

    project = FontProject()
    project.run_from_ufos(
        [ufo],
        output=["otf"],
        remove_overlaps=True,
        output_path=directory / "DraftUTN-Regular.otf",
    )

    # glyph_set = SourceGlyphSet(
    #     script=data.mongolian,
    #     font=Font.open(source_ufo_path),
    #     implied_script_codes=[Common.code, data.mongolian.code],
    #     validate_glyph_availability=False,
    # )

    # builder = glyph_set.otl_code_builder()

    # for name in data.mongolian.characters.keys():
    #     try:
    #         name = glyph_set[name]
    #     except GlyphNotInSourceFontError:
    #         continue
    #     builder.shaped_glyph_names.update([name])

    # builder.build_with_writer(otl.writer)

    # # feaLib’s include() following somehow fails.
    # inlined_otl_path = otl_dir / "stateless.fea"
    # include_statement_pattern = re.compile(r"include\((.+)\);\n")
    # with inlined_otl_path.open("w") as inlined_otl:
    #     with otl_path.open() as main_otl:
    #         for line in main_otl:
    #             if match := include_statement_pattern.fullmatch(line):
    #                 included_otl_path = otl_path.parent / match.group(1)
    #                 inlined_otl.write(included_otl_path.read_text())
    #             else:
    #                 inlined_otl.write(line)

    # legacy_script = LegacyScriptRegister.script_by_code[data.mongolian.code]
    # nnbsp = next(i for i in legacy_script.glyphs if i.formal_notation() == "Mong:nnbsp")
    # nnbsp.info.code_point = 0x202F
    # legacy_script.export_otl_dummy_font(
    #     product_dir,
    #     source_ufo_path,
    #     naming=LegacySimpleNaming,
    #     feature_file_path=inlined_otl_path,
    # )


# class LegacySimpleNaming(LegacyDevelopmentNaming):
#     @classmethod
#     def make_name(cls, identity: GlyphIdentity) -> str:
#         return super().make_name(
#             identity, implied_script_codes=[Common.code, data.mongolian.code]
#         )


if __name__ == "__main__":
    main()
