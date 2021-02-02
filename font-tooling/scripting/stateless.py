from pathlib import Path
from typing import cast

import tptqutils.otl as otl
from tptqutils.glyph import DevelopmentNaming, Identity

from data import Mongolian
from utils import make_glyph_classes, slice_joining_form


def Id(phonetic_letter: str, written_units: list[str] = None, joining_form: str = None) -> Identity:

    suffixes = []
    if written_units:
        suffixes.append(DevelopmentNaming.body(written_units))
    if joining_form:
        suffixes.append(joining_form)

    return Identity(phonetic_letter, suffix=suffixes, script_code=Mongolian.code)

def make_class_name(phonetic_letter: str, joining_form: str = None) -> str:
    return "@" + Id(phonetic_letter, joining_form=joining_form).imply_script(Mongolian.code).name()


def make_otl_code_file(builder: otl.CodeBuilder, path: Path):

    Mong = cast(Mongolian, builder.script)
    directory = path.parent

    with builder.File(directory / "classes-letters.fea") as f:
        f.comment(
            "Manual variants are excluded from these classes, as they are not needed in shaping "
            "contexts."
        )
        for name in Mong.categorization.letter:
            letter = Mong.characters[name]
            subclasses = []
            for joining_form in otl.JOINING_FORM_TAGS:
                class_name = make_class_name(name, joining_form)
                subclasses.append(class_name)
                abstract_variant = Id(name, None, joining_form)
                variants = [
                    Id(name, v.written_units, joining_form)
                    for v in letter.variants_by_joining_form.get(joining_form, [])
                    if not v.is_manual
                ]
                f.glyph_class(class_name, [abstract_variant, *variants])
            f.glyph_class(make_class_name(name), subclasses)

    with builder.File(directory / "classes-categories.fea") as f:
        for category, value in Mong.categorization.letter.immediate_members.items():
            if value:
                make_glyph_classes(f, [category], value)

    with builder.File(directory / "lookups-joining.fea") as f:
        for joining_form in otl.JOINING_FORM_TAGS:
            with f.Lookup(f"IIa.{joining_form}") as lookup:
                for name in Mong.categorization.letter:
                    lookup.sub(name, by = Id(name, None, joining_form))

    abstract_variant_to_definite = {}
    condition_to_substitutions = {}
    abstract_variant_to_fallback = {}
    joining_form_class_and_fvs_to_manual = {}
    for name in Mong.categorization.letter:
        letter = Mong.characters[name]
        for joining_form, variants in letter.variants_by_joining_form.items():
            for variant in variants:
                abstract_variant = Id(name, None, joining_form)
                variant_glyph = Id(name, variant.written_units, joining_form)
                if variant.is_definite:
                    abstract_variant_to_definite[abstract_variant] = variant_glyph
                else:
                    # Prevent the validation of contextual availability from failing in Lookup.sub:
                    builder.shaped_glyph_names[builder.glyph_space[variant_glyph]] = None
                    joining_form_class = make_class_name(name, joining_form)
                    for condition in variant.conditions:
                        if condition == "fallback":
                            abstract_variant_to_fallback[abstract_variant] = variant_glyph
                        else:
                            condition_dict = condition_to_substitutions.setdefault(condition, {})
                            condition_dict[joining_form_class] = variant_glyph
                    fvs = f"fvs{variant.fvs}"
                    joining_form_class_and_fvs_to_manual[joining_form_class, fvs] = variant_glyph

    with builder.File(directory / "lookups-conditions.fea") as f:
        for condition, substitutions in condition_to_substitutions.items():
            with f.Lookup(f"condition.{condition}") as lookup:
                for joining_form_class, variant in substitutions.items():
                    lookup.sub(joining_form_class, by=variant)

    with builder.File(directory / "lookups-general.fea") as f:

        with f.Lookup("III.ig.preprocessing.A") as lookup:
            for name in Mong.categorization.letter.vowel.masculine:
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = Id(name, None, joining_form)
                    lookup.sub(abstract_variant, by = (abstract_variant, "masculine"))

        f.glyph_class("@signal.masculine", ["masculine"])

        with f.Lookup("III.ig.preprocessing.B").flag(mark_filtering_set="@signal.masculine") as lookup:
            for name in [
                *Mong.categorization.letter.vowel.neuter,
                *Mong.categorization.letter.consonant
            ]:
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = Id(name, None, joining_form)
                    lookup.sub(prefix="masculine", target=abstract_variant, by = (abstract_variant, "masculine"))

        with f.Lookup("III.ig.preprocessing.C") as lookup:
            for name in [
                *Mong.categorization.letter.vowel.masculine,
                *Mong.categorization.letter.vowel.neuter,
                *Mong.categorization.letter.consonant,
            ]:
                if name == "g":
                    continue
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = Id(name, None, joining_form)
                    lookup.sub((abstract_variant, "masculine"), by=abstract_variant)

        f.glyph_class("@consonant.init", [
            make_class_name(name, "init") for name in Mong.categorization.letter.consonant
        ])

        with f.Lookup("III.definite") as lookup:
            for abstract, definite in abstract_variant_to_definite.items():
                lookup.sub(abstract, by=definite)

        def conditions(key: str):
            return otl.Lookup.namespace[f"condition.{key}"]

        with f.Lookup("III.a_e.chachlag").flag("IgnoreMarks") as lookup:
            # @letter.chachlag_eligible -> <chachlag> / MVS _
            lookup.sub(prefix="mvs", target=["@a.isol", "@e.isol"], chain=conditions("chachlag"))

        with f.Lookup("III.o_u_oe_ue.marked").flag("IgnoreMarks") as lookup:
            lookup.sub(prefix="@consonant.init", target=["@o", "@u", "@oe", "@ue"], chain=conditions("marked"))

        with f.Lookup("III.n_j_y_w_h_g.chachlag_onset").flag("IgnoreMarks") as lookup:
            lookup.sub(["@n", "@j", "@y", "@w"], suffix=("mvs", ["@a.isol", "@e.isol"]), chain=conditions("chachlag_onset"))
            lookup.sub(["@h", "@g"], suffix=("mvs", "@a.isol"), chain=conditions("chachlag_onset"))

        with f.Lookup("III.n_d.onset_and_devsger").flag("IgnoreMarks") as lookup:
            lookup.sub(["@n", "@d"], suffix="@vowel", chain=conditions("onset"))
            lookup.sub(prefix="@vowel", target=["@n", "@d"], chain=conditions("devsger"))

        with f.Lookup("III.h_g.onset_and_devsger_and_gender.A").flag("IgnoreMarks") as lookup:
            lookup.sub(["@h", "@g"], suffix="@vowel.masculine", chain=conditions("masculine_onset"))
            lookup.sub(["@h", "@g"], suffix=["@vowel.feminine", "@vowel.neuter"], chain=conditions("feminine"))
            lookup.sub(prefix="@vowel.masculine", target="@g", chain=conditions("masculine_devsger"))
            lookup.sub(prefix="@vowel.feminine", target="@g", chain=conditions("feminine"))

        with f.Lookup("III.h_g.onset_and_devsger_and_gender.B").flag(mark_filtering_set="@signal.masculine") as lookup:
            lookup.sub(ignore=True, target="@g", suffix="@vowel")
            lookup.sub(ignore=True, target="@g", suffix=("masculine", "@vowel"))
            lookup.sub(prefix="@i", target="@g", suffix="masculine", chain=conditions("masculine_devsger"))
            lookup.sub(prefix="@i", target="@g", chain=conditions("feminine"))

        with f.Lookup("III.ig.postprocessing") as lookup:
            name = "g"
            for joining_form, variants in Mong.characters[name].variants_by_joining_form.items():
                for variant in variants:
                    variant = Id(name, variant.written_units, joining_form)
                    lookup.sub((variant, "masculine"), by=variant)

        with f.Lookup("III.a_i_u_ue_d.particle").flag("IgnoreMarks") as lookup:
            lookup.sub(prefix="mvs", target=["@a", "@i", "@u", "@ue", "@d"], chain=conditions("particle"))
            lookup.sub(prefix=("mvs", "@consonant.init"), target=["@u", "@ue"], chain=conditions("particle"))

        with f.Lookup("III.y.dictionary_particle").flag("IgnoreMarks") as lookup:
            lookup.sub(prefix=("mvs", "i.I.init"), target="y.Y.medi", suffix=(["a.A.medi", "e.A.medi"], ["n.A.fina", "r.R.fina"]), chain=conditions("dictionary_particle"))
            lookup.sub(prefix="mvs", target="y.Y.init", suffix="i.I.fina", chain=conditions("dictionary_particle"))
            lookup.sub(prefix="mvs", target="y.Y.init", suffix=("i.I.medi", "n.A.fina"), chain=conditions("dictionary_particle"))

        # h.medi fallback is not appropriate for the undefined devsger.
        with f.Lookup("III.fallback") as lookup:
            for abstract, fallback in abstract_variant_to_fallback.items():
                lookup.sub(abstract, by=fallback)

        with f.Lookup("III.i.devsger").flag("IgnoreMarks") as lookup:
            lookup.glyph_class(context_class_name := "@vowel.not_ending_with_I", [
                Id(name, v.written_units, joining_form)
                for name in Mong.categorization.letter.vowel
                for joining_form, variants in Mong.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units[-1] != "I"
            ])
            lookup.sub(prefix=context_class_name, target="@i", chain=conditions("devsger"))

        with f.Lookup("III.o_u_oe_ue.post_bowed").flag("IgnoreMarks") as lookup:
            lookup.glyph_class(context_class_name := "@B_P_G_Gx_F_K", [
                Id(name, v.written_units, joining_form)
                for name in Mong.categorization.letter
                for joining_form, variants in Mong.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units[-1] in ["B", "P", "G", "Gx", "F", "K"]
            ])
            lookup.glyph_class(target_class_name := "@o_u_oe_ue.U", [
                Id(name, v.written_units, joining_form)
                for name in ["o", "u", "oe", "ue"]
                for joining_form, variants in Mong.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units == ["U"]
            ])
            lookup.sub(prefix=context_class_name, target=target_class_name, chain=conditions("post_bowed"))

        with f.Lookup("III.fvs") as lookup:
            for (joining_form_class, fvs), manual in joining_form_class_and_fvs_to_manual.items():
                lookup.sub(joining_form_class, suffix=fvs, by=manual)

        preserved_format_controls = [
            *Mong.categorization.format_control.mvs, *Mong.categorization.format_control.fvs
        ]
        with f.Lookup("IIb.preserve_format_controls.A") as lookup:
            for name in preserved_format_controls:
                lookup.sub(name, by = (f"_{name}", "_helper"))
        with f.Lookup("IIb.preserve_format_controls.B") as lookup:
            for name in preserved_format_controls:
                lookup.sub((f"_{name}", "_helper"), by=f"_{name}")

        # Fails to restore advance for GDEF marks in HarfBuzz. Using GSUB instead.
        with f.Lookup("IIb.restore_GDEF_mark_advances") as lookup:
            lookup.sub("masculine", by="_masculine")

    with builder.File(directory / "lookups-test.fea") as f:
        with f.Lookup("test.ss01.wipe_phonetic_information") as lookup:
            for name, letter in Mong.characters.items():
                if name not in Mong.categorization.letter:
                    continue
                for joining_form, variants in letter.variants_by_joining_form.items():
                    for variant in variants:
                        origin = Id(name, variant.written_units, joining_form)
                        parts = tuple(
                            Id(written_unit, None, sliced_joining_form)
                            for written_unit, sliced_joining_form in zip(
                                variant.written_units,
                                slice_joining_form(joining_form, len(variant.written_units)),
                            )
                        )
                        lookup.sub(origin, by=parts)

    with builder.File(path) as f:

        f.include("classes-letters.fea")
        f.include("classes-categories.fea")

        with f.Table("GDEF") as table:
            table.glyph_class_definition(
                bases=None,
                ligatures=None,
                marks = [  # Somehow cannot restore advance in dist.
                    *Mong.categorization.format_control.joining_control,
                    *Mong.categorization.format_control.fvs,
                    "masculine",
                ],
                components=None,
            )

        f.language_system(Mong.otl_tags()[0])

        f.include("lookups-joining.fea")
        for name in otl.Lookup.namespace.keys():
            stage, _, joining_form = name.partition(".")
            if stage == "IIa":
                with f.Feature(joining_form) as feature:
                    feature.lookup(name)

        f.include("lookups-conditions.fea")
        f.include("lookups-general.fea")
        with f.Feature("rclt") as feature:
            for name in otl.Lookup.namespace.keys():
                stage, *_ = name.split(".")
                if stage in ["III", "IIb"]:
                    feature.lookup(name)

        f.include("lookups-test.fea")
        for name in otl.Lookup.namespace.keys():
            stage, feature_tag, *_ = name.split(".")
            if stage == "test":
                with f.Feature(feature_tag) as feature:
                    feature.lookup(name)
