from __future__ import annotations

import functools
from itertools import chain
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NamedTuple

from tptqscripttools.data import REGISTER
from tptqscripttools.objects import DevelopmentNaming, Script
from tptqscripttools.otl import (DEFAULT_LANGUAGE_TAG, FeaFile, GlyphSpace,
                                 Writer)

from data import Category, categorization, characters, otl, written_units

scripting_path = Path(__file__)
project_dir = scripting_path.parent

data_dir = project_dir / ".." / ".." / "utn" / "data"
otl_dir = project_dir / "stateless"
product_dir = project_dir / "products"

class SimpleNaming(DevelopmentNaming):
    make_name = functools.partial(
        DevelopmentNaming.make_name, implied_script_codes = [Script.COMMON_CODE, "Mong"],
    )


def main():

    glyph_naming_scheme = SimpleNaming

    script = REGISTER.script_by_code["Mong"]
    glyph_space = script.glyph_space(source=None, naming=glyph_naming_scheme)  # not checking availability in a source glyph set

    otl_path = make_otl_file(glyph_space)
    script.export_otl_dummy_font(
        product_dir, naming=glyph_naming_scheme, feature_file_path=otl_path,
    )


def make_otl_file(glyph_space: GlyphSpace) -> Path:

    mong = glyph_space

    with FeaFile(otl_dir / "classes.fea", source=scripting_path) as file:

        classes = SimpleNamespace()

        for name in categorization.letter.members():
            classes.__dict__[name] = []
            letter = characters[name]
            for joining_form in otl.JOINING_FORM_TAGS:
                class_name = "@" + name + "." + joining_form
                classes.__dict__[name].append(class_name)
                abstract_variant = mong[name + "." + joining_form]
                variants = [
                    mong[name + "." + "_".join(v.written_units) + "." + joining_form]
                    for v in letter.variants_by_joining_form.get(joining_form, [])
                ]
                file.classDefinition(class_name, [abstract_variant] + variants)

        for name in categorization.letter.members():
            file.classDefinition("@" + name, classes.__dict__[name])

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

        class Substitution(NamedTuple):
            target: list[str]
            substitution: list[str]
            backtrack: list[str]
            lookahead: list[str]

        condition_to_substitutions = {}
        fallback_substitutions = []
        fvs_substitutions = []
        for name in categorization.letter.members():
            letter = characters[name]
            for joining_form, variants in letter.variants_by_joining_form.items():
                for variant in variants:
                    abstract_variant = mong[name + "." + joining_form]
                    sub = "@" + name + "." + joining_form
                    by = mong[name + "." + "_".join(variant.written_units) + "." + joining_form]
                    for condition in variant.conditions:
                        if condition == "fallback":
                            fallback_substitutions.append(
                                Substitution([abstract_variant], [by], backtrack=[], lookahead=[])
                            )
                        else:
                            condition_to_substitutions.setdefault(condition, {})[sub] = by
                    if fvs_int := variant.fvs:
                        fvs = mong[f"fvs{fvs_int}"]
                        fvs_substitutions.append(
                            Substitution([sub], [by], backtrack=[], lookahead=[fvs])
                        )

        lookups.condition = {}

        for condition, substitutions in condition_to_substitutions.items():
            with file.Lookup("condition." + condition) as lookup:
                lookups.condition[condition] = lookup.name
                for sub, by in substitutions.items():
                    lookup.substitution(sub, by)

        lookups.III = {}

        step = "chachlag"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            # @letter.chachlag_eligible -> <chachlag> / MVS _
            mvs = mong[categorization.format_control.mvs.members()[0]]
            lookup.raw(
                f"sub {mvs} [@a.isol @e.isol]' lookup {lookups.condition[step]};"
            )

        step = "marked"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            lookup.classDefinition("@consonant.init", [
                "@" + name + ".init" for name in categorization.letter.consonant.members()
            ])
            lookup.raw(
                f"sub @consonant.init [@o @u @oe @ue]' lookup {lookups.condition[step]};"
            )

        step = "fallback"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            for substitution in fallback_substitutions:
                lookup.substitution(*substitution)

        step = "fvs"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            for substitution in fvs_substitutions:
                lookup.substitution(*substitution)

        lookups.IIb = {}

        # To-do: Build a lookup registered to a ssXX to wipe phonetic letter information (a.AA.init -> AA.init)

    with FeaFile(otl_dir / "main.fea", source=scripting_path) as file:

        from fontTools.feaLib import ast

        table = ast.TableBlock("GDEF")
        statement = ast.GlyphClassDefStatement(
            baseGlyphs=None,
            ligatureGlyphs=None,
            markGlyphs = ast.GlyphClass(
                mong[name] for name in categorization.format_control.joining_control.members()
                + categorization.format_control.fvs.members()
            ),
            componentGlyphs=None,
        )
        table.statements.append(statement)
        file.raw(table.asFea())

        file.languageSystem(mong.script.info.otl.tags[0], DEFAULT_LANGUAGE_TAG)

        for joining_form, name in lookups.IIa.items():
            feature = file.feature(joining_form)
            feature.lookupReference(name)

        feature = file.feature("rclt")
        # feature.substitution("mvs", "sjdfiwfwo")
        for name in chain(lookups.III.values(), lookups.IIb.values()):
            feature.lookupReference(name)

    # feaLib’s include() following somehow fails.
    stitched_otl_path = project_dir / "stateless.fea"
    with stitched_otl_path.open("w") as f:
        for filename in ["classes.fea", "lookups.fea", "main.fea"]:
            f.write((otl_dir / filename).read_text() + "\n")

    return stitched_otl_path


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


if __name__ == "__main__":
    main()
