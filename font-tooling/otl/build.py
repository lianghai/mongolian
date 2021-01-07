from __future__ import annotations

import functools
import re
from itertools import chain
from pathlib import Path
from types import SimpleNamespace

from tptqscripttools.data import REGISTER
from tptqscripttools.objects import DevelopmentNaming, Script
from tptqscripttools.otl import FeaFile, GlyphSpace, Writer

from data import Category, categorization, characters, otl

scripting_path = Path(__file__)
project_dir = scripting_path.parent

otl_dir = project_dir / "stateless"
glyphs_dir = project_dir / ".." / "glyphs"
product_dir = project_dir / ".." / "products"

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

    otl_path = make_otl_file(glyph_space)

    # feaLib’s include() following somehow fails.
    inlined_otl_path = project_dir / "stateless.fea"
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


def make_otl_file(glyph_space: GlyphSpace) -> Path:

    mong = glyph_space

    with FeaFile(otl_dir / "classes.fea", source=scripting_path) as file:

        for name in categorization.letter.members():
            letter = characters[name]
            subclasses = []
            for joining_form in otl.JOINING_FORM_TAGS:
                class_name = "@" + name + "." + joining_form
                subclasses.append(class_name)
                abstract_variant = mong[name + "." + joining_form]
                variants = [
                    mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(v.written_units) + "." + joining_form]
                    for v in letter.variants_by_joining_form.get(joining_form, [])
                ]
                file.classDefinition(class_name, [abstract_variant] + variants)
            file.classDefinition("@" + name, subclasses)

        for category, value in categorization.letter._members.items():
            make_class_definitions(file, [category], value)

    lookups = SimpleNamespace()

    with FeaFile(otl_dir / "lookups.fea", source=scripting_path) as file:

        lookups.IIa = {}
        for joining_form in otl.JOINING_FORM_TAGS:
            with file.Lookup("IIa." + joining_form) as lookup:
                lookups.IIa[joining_form] = lookup.name
                for name in categorization.letter.members():
                    lookup.substitution(mong[name], mong[name + "." + joining_form])

        abstract_variant_to_definite = {}
        condition_to_substitutions = {}
        abstract_variant_to_fallback = {}
        joining_form_class_and_fvs_to_manual = {}
        for name in categorization.letter.members():
            letter = characters[name]
            for joining_form, variants in letter.variants_by_joining_form.items():
                for variant in variants:
                    abstract_variant = mong[name + "." + joining_form]
                    joining_form_class = "@" + name + "." + joining_form
                    variant_glyph = mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(variant.written_units) + "." + joining_form]
                    if not variant.conditions and not variant.fvs:
                        abstract_variant_to_definite[abstract_variant] = variant_glyph
                    else:
                        for condition in variant.conditions:
                            if condition == "fallback":
                                abstract_variant_to_fallback[abstract_variant] = variant_glyph
                            else:
                                condition_to_substitutions.setdefault(condition, {})[joining_form_class] = variant_glyph
                        fvs = mong[f"fvs{variant.fvs}"]
                        joining_form_class_and_fvs_to_manual[joining_form_class, fvs] = variant_glyph

        lookups.condition = {}

        for condition, substitutions in condition_to_substitutions.items():
            with file.Lookup("condition." + condition) as lookup:
                lookups.condition[condition] = lookup.name
                for joining_form_class, variant in substitutions.items():
                    lookup.substitution(joining_form_class, variant)

        lookups.III = {}

        file.classDefinition("@consonant.init", [
            "@" + name + ".init" for name in categorization.letter.consonant.members()
        ])

        step = "definite"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            for abstract, definite in abstract_variant_to_definite.items():
                lookup.substitution(abstract, definite)

        step = "a_e.chachlag"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            # @letter.chachlag_eligible -> <chachlag> / MVS _
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw(
                    f"sub mvs [@a.isol @e.isol]' lookup {lookups.condition['chachlag']};"
                )

        step = "o_u_oe_ue.marked"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw(
                    f"sub @consonant.init [@o @u @oe @ue]' lookup {lookups.condition['marked']};"
                )

        step = "n_j_y_w_h_g.chachlag_onset"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw([
                    f"sub [@n @j @y @w]' lookup {lookups.condition['chachlag_onset']} mvs [@a.isol @e.isol];",
                    f"sub [@h @g]' lookup {lookups.condition['chachlag_onset']} mvs [@a.isol];",
                ])

        step = "n_d.onset_and_devsger"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw([
                    f"sub [@n @d]' lookup {lookups.condition['onset']} @vowel;",
                    f"sub @vowel [@n @d]' lookup {lookups.condition['devsger']};",
                ])

        step = "h_g.onset_and_devsger_and_gender"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw([
                    f"sub [@h @g]' lookup {lookups.condition['masculine_onset']} @vowel.masculine;",
                    f"sub [@h @g]' lookup {lookups.condition['feminine']} [@vowel.feminine @vowel.neuter];",
                    f"sub @vowel.masculine @g' lookup {lookups.condition['masculine_devsger']};",
                    f"sub @vowel.feminine @g' lookup {lookups.condition['feminine']};",
                    f"sub @vowel.masculine @consonant @i @g' lookup {lookups.condition['masculine_devsger']};",  # To be completed
                    f"sub @g' lookup {lookups.condition['feminine']};",
                ])

        step = "a_i_u_ue_d.particle"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw([
                    f"sub mvs [@a @i @u @ue @d]' lookup {lookups.condition['particle']};",
                    f"sub mvs @consonant.init [@u @ue]' lookup {lookups.condition['particle']};",
                ])

        step = "y.dictionary_particle"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.raw([
                    f"sub mvs i.I.init y.Y.medi' lookup {lookups.condition['dictionary_particle']} [a.A.medi e.A.medi] [n.A.fina r.R.fina];",
                    f"sub mvs y.Y.init' lookup {lookups.condition['dictionary_particle']} i.I.fina;",
                    f"sub mvs y.Y.init' lookup {lookups.condition['dictionary_particle']} i.I.medi n.A.fina;",
                ])

        step = "fallback"
        # h.medi fallback is not appropriate for the undefined devsger.
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            for abstract, fallback in abstract_variant_to_fallback.items():
                lookup.substitution(abstract, fallback)

        step = "fvs"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            for (joining_form_class, fvs), manual in joining_form_class_and_fvs_to_manual.items():
                lookup.substitution(joining_form_class, manual, lookahead=[fvs])

        lookups.IIb = {}

        preserved_format_controls = [
            mong[name] for name in categorization.format_control.mvs.members()
            + categorization.format_control.fvs.members()
        ]
        step = "preserve_format_controls.A"
        with file.Lookup("IIb." + step) as lookup:
            lookups.IIb[step] = lookup.name
            for name in preserved_format_controls:
                lookup.substitution(name, [f"_{name}", "_"])
        step = "preserve_format_controls.B"
        with file.Lookup("IIb." + step) as lookup:
            lookups.IIb[step] = lookup.name
            for name in preserved_format_controls:
                lookup.substitution([f"_{name}", "_"], name)

        # Fails to restore advance in HarfBuzz. Shifting x placement works.
        # lookups.dist = {}
        # step = "restore_advance"
        # with file.Lookup("IIb." + step) as lookup:
        #     lookups.dist[step] = lookup.name
        #     from fontTools.ufoLib.glifLib import Glyph
        #     glyph_object = Glyph(None, None)
        #     mong.source.getGlyphSet().readGlyph("nirugu", glyph_object)
        #     lookup.raw(f"pos nirugu {glyph_object.width};")
        #     lookup.raw("pos fvs1 <500 0 500 0>;")

        lookups.stylistic = {}
        tag = "ss01"
        with file.Lookup("test." + "wipe_phonetic_information") as lookup:
            lookups.stylistic[tag] = lookup.name
            for name, letter in characters.items():
                if name not in categorization.letter.members():
                    continue
                for joining_form, variants in letter.variants_by_joining_form.items():
                    for variant in variants:
                        lookup.substitution(
                            mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(variant.written_units) + "." + joining_form],
                            [mong[".".join([wu, sliced_joining_form])] for wu, sliced_joining_form in zip(variant.written_units, slice_joining_form(joining_form, len(variant.written_units)))],
                        )

    main_otl_path = otl_dir / "main.fea"
    with FeaFile(main_otl_path, source=scripting_path) as file:

        file.raw("include(classes.fea);")

        from fontTools.feaLib import ast

        table = ast.TableBlock("GDEF")
        table.statements = [
            ast.GlyphClassDefStatement(
                baseGlyphs=None,
                ligatureGlyphs=ast.GlyphClass(
                    mong[name] for name in categorization.format_control.joining_control.members()
                    + categorization.format_control.fvs.members()
                ),
                markGlyphs=None,  # Somehow cannot restore advance in hist.
                componentGlyphs=None,
            ),
        ]
        file.raw(table.asFea())

        file.languageSystem(mong.script.info.otl.tags[0], otl.DEFAULT_LANGUAGE_TAG)

        file.raw("include(lookups.fea);")

        for joining_form, name in lookups.IIa.items():
            feature = file.feature(joining_form)
            feature.lookupReference(name)

        feature = file.feature("rclt")
        for name in chain(lookups.III.values(), lookups.IIb.values()):
            feature.lookupReference(name)

        # feature = file.feature("dist")
        # for name in lookups.dist.values():
        #     feature.lookupReference(name)

        for tag, name in lookups.stylistic.items():
            feature = file.feature(tag)
            feature.lookupReference(name)

    return main_otl_path


def make_class_definitions(writer: Writer, category_chain: list[str], category: Category):

    class_name = "@" + ".".join(category_chain)
    members = []
    if isinstance(category._members, dict):
        for sub_category, value in category._members.items():
            sub_category_chain = category_chain[:] + [sub_category]
            nested_class_name = "@" + ".".join(sub_category_chain)
            make_class_definitions(writer, sub_category_chain, value)
            members.append(nested_class_name)
    elif isinstance(category._members, list):
        members.extend("@" + i for i in category._members)

    if members:
        writer.classDefinition(class_name, members)


def slice_joining_form(joining_form: str, slice_into: int) -> list[str]:
    name_to_joinedness = {
        "isol": (False, False),
        "init": (False, True),
        "medi": (True, True),
        "fina": (True, False),
    }
    joinedness_to_name = {v: k for k, v in name_to_joinedness.items()}
    is_joined_before, is_joined_after = name_to_joinedness[joining_form]
    joining_forms = []
    if slice_into == 1:
        joining_forms.append(joining_form)
    elif slice_into > 1:
        for i in range(slice_into):
            if i == 0:
                joining_forms.append(joinedness_to_name[(is_joined_before, True)])
            elif i == slice_into - 1:
                joining_forms.append(joinedness_to_name[(True, is_joined_after)])
            else:
                joining_forms.append(joinedness_to_name[(True, True)])
    return joining_forms


if __name__ == "__main__":
    main()
