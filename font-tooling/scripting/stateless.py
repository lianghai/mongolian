from itertools import chain
from pathlib import Path

from fontTools.feaLib import ast
from tptqscripttools.otl import FeaFile, GlyphSpace, Writer

from data import categorization, characters, otl
from utils import make_class_definitions, slice_joining_form


def make_otl_file(scripting_path: Path, otl_path: Path, glyph_space: GlyphSpace):

    mong = glyph_space

    def make_name(
        phonetic_letter: str, written_units: list[str] = None, joining_form: str = None,
    ) -> str:
        return glyph_space.naming.VARIATION_SUFFIX_LEADER.join(filter(None, [
            phonetic_letter,
            glyph_space.naming.COMPONENT_SEP.join(written_units or []),
            joining_form,
        ]))

    with FeaFile(otl_path.parent / "classes-letters.fea", source=scripting_path) as f:
        for name in categorization.letter.members():
            letter = characters[name]
            subclasses = []
            for joining_form in otl.JOINING_FORM_TAGS:
                class_name = "@" + make_name(name, None, joining_form)
                subclasses.append(class_name)
                abstract_variant = mong[make_name(name, None, joining_form)]
                variants = [
                    mong[make_name(name, v.written_units, joining_form)]
                    for v in letter.variants_by_joining_form.get(joining_form, [])
                ]
                f.classDefinition(class_name, [abstract_variant] + variants)
            f.classDefinition("@" + name, subclasses)

    with FeaFile(otl_path.parent / "classes-categories.fea", source=scripting_path) as f:
        for category, value in categorization.letter.immediate_members.items():
            if value:
                make_class_definitions(f, [category], value)

    with FeaFile(otl_path.parent / "lookups-joining.fea", source=scripting_path) as f:
        for joining_form in otl.JOINING_FORM_TAGS:
            with f.Lookup(["IIa", joining_form]) as lookup:
                for name in categorization.letter.members():
                    lookup.substitution(mong[name], mong[make_name(name, None, joining_form)])

    abstract_variant_to_definite = {}
    condition_to_substitutions = {}
    abstract_variant_to_fallback = {}
    joining_form_class_and_fvs_to_manual = {}
    for name in categorization.letter.members():
        letter = characters[name]
        for joining_form, variants in letter.variants_by_joining_form.items():
            for variant in variants:
                abstract_variant = mong[make_name(name, None, joining_form)]
                joining_form_class = "@" + make_name(name, None, joining_form)
                variant_glyph = mong[make_name(name, variant.written_units, joining_form)]
                if not variant.conditions and not variant.fvs:
                    abstract_variant_to_definite[abstract_variant] = variant_glyph
                else:
                    for condition in variant.conditions:
                        if condition == "fallback":
                            abstract_variant_to_fallback[abstract_variant] = variant_glyph
                        else:
                            condition_to_substitutions.setdefault(condition, {})[
                                joining_form_class
                            ] = variant_glyph
                    fvs = mong[f"fvs{variant.fvs}"]
                    joining_form_class_and_fvs_to_manual[joining_form_class, fvs] = variant_glyph

    lookups = Writer.lookup_namespace

    with FeaFile(otl_path.parent / "lookups-conditions.fea", source=scripting_path) as f:
        for condition, substitutions in condition_to_substitutions.items():
            with f.Lookup(["condition", condition]) as lookup:
                for joining_form_class, variant in substitutions.items():
                    lookup.substitution(joining_form_class, variant)

    with FeaFile(otl_path.parent / "lookups-general.fea", source=scripting_path) as f:

        f.classDefinition("@consonant.init", [
            "@" + name + ".init" for name in categorization.letter.consonant.members()
        ])

        with f.Lookup(["III", "definite"]) as lookup:
            for abstract, definite in abstract_variant_to_definite.items():
                lookup.substitution(abstract, definite)

        with f.Lookup(["III", "a_e.chachlag"], flag="IgnoreLigatures") as lookup:
            # @letter.chachlag_eligible -> <chachlag> / MVS _
            lookup.raw(f"sub mvs [@a.isol @e.isol]' lookup {lookups.condition['chachlag']};")

        with f.Lookup(["III", "o_u_oe_ue.marked"], flag="IgnoreLigatures") as lookup:
            lookup.raw(
                f"sub @consonant.init [@o @u @oe @ue]' lookup {lookups.condition['marked']};"
            )

        with f.Lookup(["III", "n_j_y_w_h_g.chachlag_onset"], flag="IgnoreLigatures") as lookup:
            lookup.raw([
                f"sub [@n @j @y @w]' lookup {lookups.condition['chachlag_onset']} mvs [@a.isol @e.isol];",
                f"sub [@h @g]' lookup {lookups.condition['chachlag_onset']} mvs [@a.isol];",
            ])

        with f.Lookup(["III", "n_d.onset_and_devsger"], flag="IgnoreLigatures") as lookup:
            lookup.raw([
                f"sub [@n @d]' lookup {lookups.condition['onset']} @vowel;",
                f"sub @vowel [@n @d]' lookup {lookups.condition['devsger']};",
            ])

        # with f.Lookup(["III", "h_g.onset_and_devsger_and_gender.preprocessing"]) as lookup:
        #     pass

        with f.Lookup(["III", "h_g.onset_and_devsger_and_gender"], flag="IgnoreLigatures") as lookup:
            lookup.raw([
                f"sub [@h @g]' lookup {lookups.condition['masculine_onset']} @vowel.masculine;",
                f"sub [@h @g]' lookup {lookups.condition['feminine']} [@vowel.feminine @vowel.neuter];",
                f"sub @vowel.masculine @g' lookup {lookups.condition['masculine_devsger']};",
                f"sub @vowel.feminine @g' lookup {lookups.condition['feminine']};",
                f"sub @vowel.masculine @consonant @i @g' lookup {lookups.condition['masculine_devsger']};",
                f"sub @g' lookup {lookups.condition['feminine']};",
            ])

        with f.Lookup(["III", "a_i_u_ue_d.particle"], flag="IgnoreLigatures") as lookup:
            lookup.raw([
                f"sub mvs [@a @i @u @ue @d]' lookup {lookups.condition['particle']};",
                f"sub mvs @consonant.init [@u @ue]' lookup {lookups.condition['particle']};",
            ])

        with f.Lookup(["III", "y.dictionary_particle"], flag="IgnoreLigatures") as lookup:
            lookup.raw([
                f"sub mvs i.I.init y.Y.medi' lookup {lookups.condition['dictionary_particle']} [a.A.medi e.A.medi] [n.A.fina r.R.fina];",
                f"sub mvs y.Y.init' lookup {lookups.condition['dictionary_particle']} i.I.fina;",
                f"sub mvs y.Y.init' lookup {lookups.condition['dictionary_particle']} i.I.medi n.A.fina;",
            ])

        # h.medi fallback is not appropriate for the undefined devsger.
        with f.Lookup(["III", "fallback"]) as lookup:
            for abstract, fallback in abstract_variant_to_fallback.items():
                lookup.substitution(abstract, fallback)

        with f.Lookup(["III", "i.devsger"], flag="IgnoreLigatures") as lookup:
            lookup.classDefinition(context_class_name := "@vowel.not_ending_with_I", [
                mong[make_name(name, variant.written_units, joining_form)]
                for name in categorization.letter.vowel.members()
                for joining_form, variants in characters[name].variants_by_joining_form.items()
                for variant in variants
                if variant.written_units[-1] != "I"
            ])
            lookup.raw(f"sub {context_class_name} @i' lookup {lookups.condition['devsger']};")

        with f.Lookup(["III", "o_u_oe_ue.post_bowed"], flag="IgnoreLigatures") as lookup:
            lookup.classDefinition(context_class_name := "@B_P_G_Gx_F_K", [
                mong[make_name(name, variant.written_units, joining_form)]
                for name in categorization.letter.members()
                for joining_form, variants in characters[name].variants_by_joining_form.items()
                for variant in variants
                if variant.written_units[-1] in ["B", "P", "G", "Gx", "F", "K"]
            ])
            lookup.classDefinition(target_class_name := "@o_u_oe_ue.U", [
                mong[make_name(name, variant.written_units, joining_form)]
                for name in ["o", "u", "oe", "ue"]
                for joining_form, variants in characters[name].variants_by_joining_form.items()
                for variant in variants
                if variant.written_units == ["U"]
            ])
            lookup.raw(f"sub {context_class_name} {target_class_name}' lookup {lookups.condition['post_bowed']};")

        with f.Lookup(["III", "fvs"]) as lookup:
            for (joining_form_class, fvs), manual in joining_form_class_and_fvs_to_manual.items():
                lookup.substitution(joining_form_class, manual, lookahead=[fvs])

        preserved_format_controls = [
            mong[name] for name in categorization.format_control.mvs.members()
            + categorization.format_control.fvs.members()
        ]
        with f.Lookup(["IIb", "preserve_format_controls.A"]) as lookup:
            for name in preserved_format_controls:
                lookup.substitution(name, [f"_{name}", "_helper"])
        with f.Lookup(["IIb", "preserve_format_controls.B"]) as lookup:
            for name in preserved_format_controls:
                lookup.substitution([f"_{name}", "_helper"], name)

        # Fails to restore advance in HarfBuzz. Shifting x placement works. Use GSUB instead?
        # with f.Lookup(["dist", "restore_advance"]) as lookup:
        #     from fontTools.ufoLib.glifLib import Glyph
        #     glyph_object = Glyph(None, None)
        #     mong.source.getGlyphSet().readGlyph("nirugu", glyph_object)
        #     lookup.raw(f"pos nirugu {glyph_object.width};")
        #     lookup.raw("pos fvs1 <500 0 500 0>;")

    with FeaFile(otl_path.parent / "lookups-test.fea", source=scripting_path) as f:
        with f.Lookup(["test", "wipe_phonetic_information"], key="ss01") as lookup:
            for name, letter in characters.items():
                if name not in categorization.letter.members():
                    continue
                for joining_form, variants in letter.variants_by_joining_form.items():
                    for variant in variants:
                        lookup.substitution(
                            mong[make_name(name, variant.written_units, joining_form)],
                            [
                                mong[".".join([wu, sliced_joining_form])]
                                for wu, sliced_joining_form in zip(
                                    variant.written_units,
                                    slice_joining_form(joining_form, len(variant.written_units)),
                                )
                            ],
                        )

    with FeaFile(otl_path, source=scripting_path) as f:

        f.include("classes-letters.fea")
        f.include("classes-categories.fea")

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
        f.raw(table.asFea())

        f.languageSystem(mong.script.info.otl.tags[0], otl.DEFAULT_LANGUAGE_TAG)

        f.include("lookups-joining.fea")

        for joining_form, name in lookups.IIa.items():
            feature = f.feature(joining_form)
            feature.lookupReference(name)

        f.include("lookups-conditions.fea")
        f.include("lookups-general.fea")

        feature = f.feature("rclt")
        for name in chain(lookups.III.values(), lookups.IIb.values()):
            feature.lookupReference(name)

        # feature = f.feature("dist")
        # for name in lookups.dist.values():
        #     feature.lookupReference(name)

        f.include("lookups-test.fea")

        for tag, name in lookups.test.items():
            feature = f.feature(tag)
            feature.lookupReference(name)
