from itertools import chain
from pathlib import Path
from types import SimpleNamespace

from tptqscripttools.otl import FeaFile, GlyphSpace

from data import categorization, characters, otl
from utils import make_class_definitions, slice_joining_form


def make_otl_file(scripting_path: Path, otl_path: Path, glyph_space: GlyphSpace):

    mong = glyph_space

    with FeaFile(otl_path.parent / "classes-letters.fea", source=scripting_path) as file:
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

    with FeaFile(otl_path.parent / "classes-categories.fea", source=scripting_path) as file:
        for category, value in categorization.letter._members.items():
            make_class_definitions(file, [category], value)

    lookups = SimpleNamespace()

    lookups.IIa = {}
    with FeaFile(otl_path.parent / "lookups-joining.fea", source=scripting_path) as file:
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
    with FeaFile(otl_path.parent / "lookups-conditions.fea", source=scripting_path) as file:
        for condition, substitutions in condition_to_substitutions.items():
            with file.Lookup("condition." + condition) as lookup:
                lookups.condition[condition] = lookup.name
                for joining_form_class, variant in substitutions.items():
                    lookup.substitution(joining_form_class, variant)

    lookups.III = {}
    with FeaFile(otl_path.parent / "lookups-general.fea", source=scripting_path) as file:

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

        step = "i.devsger"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.classDefinition(context_class_name := "@vowel.not_ending_with_I", [
                    mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(variant.written_units) + "." + joining_form]
                    for name in categorization.letter.vowel.members()
                    for joining_form, variants in characters[name].variants_by_joining_form.items()
                    for variant in variants
                    if variant.written_units[-1] != "I"
                ])
                flagged.raw(f"sub {context_class_name} @i' lookup {lookups.condition['devsger']};")

        step = "o_u_oe_ue.post_bowed"
        with file.Lookup("III." + step) as lookup:
            lookups.III[step] = lookup.name
            with lookup.set_lookup_flag("IgnoreLigatures") as flagged:
                flagged.classDefinition(context_class_name := "@B_P_G_Gx_F_K", [
                    mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(variant.written_units) + "." + joining_form]
                    for name in categorization.letter.members()
                    for joining_form, variants in characters[name].variants_by_joining_form.items()
                    for variant in variants
                    if variant.written_units[-1] in ["B", "P", "G", "Gx", "F", "K"]
                ])
                flagged.classDefinition(target_class_name := "@o_u_oe_ue.U", [
                    mong[name + "." + glyph_space.naming.COMPONENT_SEP.join(variant.written_units) + "." + joining_form]
                    for name in ["o", "u", "oe", "ue"]
                    for joining_form, variants in characters[name].variants_by_joining_form.items()
                    for variant in variants
                    if variant.written_units == ["U"]
                ])
                flagged.raw(f"sub {context_class_name} {target_class_name}' lookup {lookups.condition['post_bowed']};")

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
                lookup.substitution(name, [f"_{name}", "_helper"])
        step = "preserve_format_controls.B"
        with file.Lookup("IIb." + step) as lookup:
            lookups.IIb[step] = lookup.name
            for name in preserved_format_controls:
                lookup.substitution([f"_{name}", "_helper"], name)

        # Fails to restore advance in HarfBuzz. Shifting x placement works. Use GSUB instead?
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
    with FeaFile(otl_path.parent / "lookups-test.fea", source=scripting_path) as file:
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

    with FeaFile(otl_path, source=scripting_path) as file:

        file.raw("include(classes-letters.fea);")
        file.raw("include(classes-categories.fea);")

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

        file.raw("include(lookups-joining.fea);")

        for joining_form, name in lookups.IIa.items():
            feature = file.feature(joining_form)
            feature.lookupReference(name)

        file.raw("include(lookups-conditions.fea);")
        file.raw("include(lookups-general.fea);")

        feature = file.feature("rclt")
        for name in chain(lookups.III.values(), lookups.IIb.values()):
            feature.lookupReference(name)

        # feature = file.feature("dist")
        # for name in lookups.dist.values():
        #     feature.lookupReference(name)

        file.raw("include(lookups-test.fea);")

        for tag, name in lookups.stylistic.items():
            feature = file.feature(tag)
            feature.lookupReference(name)
