from pathlib import Path

import tptq.utils.otl as otl
from tptq.utils.glyph import DevelopmentNaming, Identity
from tptq.utils.otl import File

from data import Category, mongolian
from utils import slice_joining_form

project_dir = Path(__file__).parent / ".."
directory = project_dir / "otl"
path = directory / "stateless" / "main.fea"


def mong(phonetic_letter: str, written_units: list[str] = None, joining_form: str = None) -> Identity:
    suffixes = []
    if written_units:
        suffixes.append(DevelopmentNaming.body(written_units))
    if joining_form:
        suffixes.append(joining_form)
    return Identity(phonetic_letter, suffix=suffixes, script_code=mongolian.code)

def make_class_name(phonetic_letter: str, joining_form: str = None) -> str:
    return "@" + mong(phonetic_letter, joining_form=joining_form).imply_script(mongolian.code).name()


def make_glyph_classes(file: File, category_chain: list[str], category: Category):

    class_name = "@" + ".".join(category_chain)
    members = []

    for key, value in category.immediate_members.items():
        if value:
            sub_category_chain = category_chain[:] + [key]
            nested_class_name = "@" + ".".join(sub_category_chain)
            make_glyph_classes(file, sub_category_chain, value)
            members.append(nested_class_name)
        else:
            members.append("@" + key)

    if members:
        file.glyph_class(class_name, members)


def writer(builder: otl.CodeBuilder):

    format_control = mongolian.categorization.format_control
    directory = path.parent

    def class_content(class_name: str):
        definition = builder.glyph_class_namespace[class_name]
        return builder._expand_glyph_class_to_names(definition.glyphs)

    with builder.File(directory / "classes-letters.fea") as f:
        f.comment(
            "Definite and manual variants are excluded from these classes, as they are not needed "
            "in shaping contexts."
        )
        for name, letter in mongolian.characters.items():
            if name not in mongolian.categorization.letter:
                continue
            subclasses = []
            for joining_form in otl.JOINING_FORM_TAGS:
                class_name = make_class_name(name, joining_form)
                subclasses.append(class_name)
                abstract_variant = mong(name, None, joining_form)
                variants = [
                    mong(name, v.written_units, joining_form)
                    for v in letter.variants_by_joining_form.get(joining_form, [])
                    if v.is_contextual
                ]
                f.glyph_class(class_name, [abstract_variant, *variants])
            f.glyph_class(make_class_name(name), subclasses)

    with builder.File(directory / "classes-categories.fea") as f:
        for category, value in mongolian.categorization.letter.immediate_members.items():
            if value:
                make_glyph_classes(f, [category], value)

    with builder.File(directory / "lookups-joining.fea") as f:
        for joining_form in otl.JOINING_FORM_TAGS:
            with f.Lookup(f"IIa.{joining_form}") as lookup:
                for name in mongolian.categorization.letter:
                    lookup.sub(name).by(mong(name, None, joining_form))

    abstract_variant_to_definite = {}
    condition_to_substitutions = dict[str, dict[tuple[str, tuple[Identity, ...]], Identity]]()
    abstract_variant_to_fallback = {}
    affected_variants_and_fvs_to_manual = dict[tuple[str, tuple[Identity, ...], str], Identity]()
    for name in mongolian.categorization.letter:
        letter = mongolian.characters[name]
        for joining_form, variants in letter.variants_by_joining_form.items():
            for variant in variants:
                abstract_variant = mong(name, None, joining_form)
                variant_glyph = mong(name, variant.written_units, joining_form)
                if variant.is_definite:
                    abstract_variant_to_definite[abstract_variant] = variant_glyph
                else:
                    # Prevent the validation of contextual availability from failing in Lookup.sub:
                    builder.shaped_glyph_names.update([builder.source_glyph_set[variant_glyph]])
                    joining_form_class_name = make_class_name(name, joining_form)
                    affected_variants: tuple[Identity, ...] = tuple(
                        [abstract_variant] + [
                            identity for variant in variants
                            if (identity := mong(name, variant.written_units, joining_form)) != variant_glyph
                            and not variant.is_manual
                        ]
                    )
                    for condition in variant.conditions:
                        if condition == "fallback":
                            abstract_variant_to_fallback[abstract_variant] = variant_glyph
                        else:
                            substitutions = condition_to_substitutions.setdefault(condition, {})
                            substitutions[joining_form_class_name, affected_variants] = variant_glyph
                    fvs = f"fvs{variant.fvs}"
                    affected_variants_and_fvs_to_manual[
                        joining_form_class_name, affected_variants, fvs,
                    ] = variant_glyph

    with builder.File(directory / "lookups-conditions.fea") as f:
        for condition, substitutions in condition_to_substitutions.items():
            with f.Lookup(f"condition.{condition}") as lookup:
                for (joining_form_class_name, affected_variants), variant in substitutions.items():
                    class_name = f"{joining_form_class_name}.for_{condition}"
                    f.glyph_class(class_name, [*affected_variants])
                    lookup.sub(class_name).by(variant)

    format_controls = [*format_control.mvs, *format_control.nnbsp, *format_control.fvs]
    effective_format_controls = [f"{i}.effective" for i in format_controls]

    with builder.File(directory / "lookups-general.fea") as f:

        with f.Lookup("III.ig.preprocessing.A") as lookup:
            for name in mongolian.categorization.letter.vowel.masculine:
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = mong(name, None, joining_form)
                    lookup.sub(abstract_variant).by(abstract_variant, "masculine")

        f.glyph_class("@signal.masculine", ["masculine"])

        with f.Lookup("III.ig.preprocessing.B").flag(mark_filtering_set="@signal.masculine") as lookup:
            for name in [
                *mongolian.categorization.letter.vowel.neuter,
                *mongolian.categorization.letter.consonant
            ]:
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = mong(name, None, joining_form)
                    lookup.prefix("masculine").sub(abstract_variant).by(abstract_variant, "masculine")

        with f.Lookup("III.ig.preprocessing.C") as lookup:
            for name in [
                *mongolian.categorization.letter.vowel.masculine,
                *mongolian.categorization.letter.vowel.neuter,
                *mongolian.categorization.letter.consonant,
            ]:
                if name == "g":
                    continue
                for joining_form in otl.JOINING_FORM_TAGS:
                    abstract_variant = mong(name, None, joining_form)
                    # lookup.sub(abstract_variant, "masculine").by(abstract_variant)
                    lookup.sub(abstract_variant, "masculine").by(abstract_variant)

        f.glyph_class("@consonant.init", [
            make_class_name(name, "init") for name in mongolian.categorization.letter.consonant
        ])

        def conditions(key: str):
            return otl.Lookup.namespace[f"condition.{key}"]

        def for_condition(condition: str, class_names: list[str]) -> list[str]:
            processed_names = []
            for name in class_names:
                names_with_joining_form_tag = []
                if name.endswith(otl.JOINING_FORM_TAGS):
                    names_with_joining_form_tag.append(name)
                else:
                    names_with_joining_form_tag.extend(
                        names_with_joining_form_tag.append(f"{name}.{tag}")
                        for tag in otl.JOINING_FORM_TAGS
                    )
                for name in names_with_joining_form_tag:
                    processed = f"{name}.for_{condition}"
                    if builder.glyph_class_namespace.get(processed):
                        processed_names.append(processed)
            return processed_names

        with f.Lookup("_.effective") as _effective:
            for origin, effective in zip(format_controls, effective_format_controls):
                _effective.sub(origin).by(effective)

        with f.Lookup("III.a_e.chachlag").flag("IgnoreMarks") as lookup:
            # @letter.chachlag_eligible -> <chachlag> / MVS _
            c = "chachlag"
            lookup.sub("mvs", for_condition(c, ["@a", "@e"])).chain(_effective, conditions(c))  # type: ignore

        with f.Lookup("III.o_u_oe_ue.marked").flag("IgnoreMarks") as lookup:
            lookup.prefix("@consonant.init").sub(["@o", "@u", "@oe", "@ue"]).chain(conditions("marked"))

        with f.Lookup("III.n_j_y_w_h_g.chachlag_onset").flag("IgnoreMarks") as lookup:
            c = "chachlag_onset"
            lookup.sub(for_condition(c, ["@n", "@j", "@y", "@w"])).suffix("mvs.effective", ["a.Aa.isol", "e.Aa.isol"]).chain(conditions(c))  # type: ignore
            lookup.sub(for_condition(c, ["@h", "@g"])).suffix("mvs.effective", "a.Aa.isol").chain(conditions(c))  # type: ignore

        with f.Lookup("III.n_t_d.onset_and_devsger").flag("IgnoreMarks") as lookup:
            lookup.sub(["@n", "@t", "@d"]).chain(conditions("onset")).suffix("@vowel")
            lookup.prefix("@vowel").sub(["@n", "@d"]).chain(conditions("devsger"))

        with f.Lookup("III.h_g.onset_and_devsger_and_gender.A").flag("IgnoreMarks") as lookup:
            lookup.sub(["@h", "@g"]).chain(conditions("masculine_onset")).suffix("@vowel.masculine")
            lookup.sub(["@h", "@g"]).chain(conditions("feminine")).suffix(["@vowel.feminine", "@vowel.neuter"])
            lookup.prefix("@vowel.masculine").sub("@g").chain(conditions("masculine_devsger"))
            lookup.prefix("@vowel.feminine").sub("@g").chain(conditions("feminine"))

        with f.Lookup("III.h_g.onset_and_devsger_and_gender.B").flag(mark_filtering_set="@signal.masculine") as lookup:
            lookup.ignore().sub("@g").suffix("@vowel")
            lookup.ignore().sub("@g").suffix("masculine", "@vowel")
            lookup.prefix("@i").sub("@g").chain(conditions("masculine_devsger")).suffix("masculine")
            lookup.prefix("@i").sub("@g").chain(conditions("feminine"))

        with f.Lookup("III.ig.postprocessing") as lookup:
            name = "g"
            for joining_form, variants in mongolian.characters[name].variants_by_joining_form.items():
                for variant in variants:
                    variant = mong(name, variant.written_units, joining_form)
                    lookup.sub(variant, "masculine").by(variant)

        with f.Lookup("III.a_i_u_ue_d.particle.A").flag("IgnoreMarks") as lookup:
            c = "particle"
            lookup.sub(["mvs", "nnbsp"], for_condition(c, ["@a.init", "@i", "@u", "@ue", "@d"])).chain(_effective, conditions(c))  # type: ignore

        with f.Lookup("III.a_i_u_ue_d.particle.B").flag("IgnoreMarks") as lookup:
            c = "particle"
            # Including .effective because @consonant.init may be a partical-initial d.
            lookup.sub(["mvs", "mvs.effective", "nnbsp", "nnbsp.effective"], "@consonant.init", for_condition(c, ["@u.fina", "@ue.medi", "@ue.fina"])).chain(_effective, None, conditions(c))  # type: ignore

        with f.Lookup("III.definite") as lookup:
            for abstract, definite in abstract_variant_to_definite.items():
                lookup.sub(abstract).by(definite)

        # h.medi fallback is not appropriate for the undefined devsger.
        with f.Lookup("III.fallback") as lookup:
            for abstract, fallback in abstract_variant_to_fallback.items():
                lookup.sub(abstract).by(fallback)

        with f.Lookup("III.y.dictionary_particle").flag("IgnoreMarks") as lookup:

            c = "dictionary_particle"

            # Hack for aligning shaping with the EAC model:
            lookup.prefix(["mvs.effective", "nnbsp.effective"]).sub("ue.O.init").by("ue.A_O_I.init").suffix("g.G.medi", "e.A.medi", "i.I.fina")

            lookup.prefix(["mvs.effective", "nnbsp.effective"], "i.I.init").sub("y.Y.medi").chain(conditions(c)).suffix(["a.A.medi", "e.A.medi"], ["n.A.fina", "r.R.fina"])
            lookup.sub(["mvs", "nnbsp"], "y.Y.init").chain(_effective, conditions(c)).suffix("i.I.fina")
            lookup.sub(["mvs", "nnbsp"], "y.Y.init").chain(_effective, conditions(c)).suffix("i.I.medi", "n.A.fina")

        with f.Lookup("III.i.devsger").flag("IgnoreMarks") as lookup:
            lookup.glyph_class(context_class_name := "@vowel.not_ending_with_I", [
                mong(name, v.written_units, joining_form)
                for name in mongolian.categorization.letter.vowel
                for joining_form, variants in mongolian.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units[-1] != "I"
            ])
            lookup.prefix(context_class_name).sub("@i").chain(conditions("devsger"))

        with f.Lookup("III.o_u_oe_ue.post_bowed").flag("IgnoreMarks") as lookup:
            lookup.glyph_class(context_class_name := "@B_P_G_Gx_F_K", [
                mong(name, v.written_units, joining_form)
                for name in mongolian.categorization.letter
                for joining_form, variants in mongolian.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units[-1] in ["B", "P", "G", "Gx", "F", "K"]
            ])
            lookup.glyph_class(target_class_name := "@o_u_oe_ue.U", [
                mong(name, v.written_units, joining_form)
                for name in ["o", "u", "oe", "ue"]
                for joining_form, variants in mongolian.characters[name].variants_by_joining_form.items()
                for v in variants
                if (not v.is_manual) and v.written_units == ["U"]
            ])
            lookup.prefix(context_class_name).sub(target_class_name).chain(conditions("post_bowed"))

        with f.Lookup("III.fvs") as lookup:

            with f.Lookup("_.manual") as _manual:
                for (joining_form_class_name, affected_variants, fvs), manual in affected_variants_and_fvs_to_manual.items():
                    class_name = f"{joining_form_class_name}.for_{fvs}"
                    f.glyph_class(class_name, [*affected_variants])
                    _manual.sub(class_name).suffix(fvs).by(manual)

            for (joining_form_class_name, _, fvs), manual in affected_variants_and_fvs_to_manual.items():
                class_name = f"{joining_form_class_name}.for_{fvs}"
                lookup.sub(class_name, fvs).chain(_manual, _effective)

        with f.Lookup("IIb.hide_effective_format_controls") as lookup:
            for name in effective_format_controls:
                if name == "nnbsp.effective":
                    lookup.sub(name).by("nnbsp")
                else:
                    lookup.sub(name).by("nil")

        preserved_format_controls = [*format_control.mvs, *format_control.nnbsp, *format_control.fvs, "nil"]
        with f.Lookup("IIb.preserve_format_controls.A") as lookup:
            for name in preserved_format_controls:
                lookup.sub(name).by(f"_{name}", "_helper")
        with f.Lookup("IIb.preserve_format_controls.B") as lookup:
            for name in preserved_format_controls:
                lookup.sub(f"_{name}", "_helper").by(f"_{name}")

        # Fails to restore advance for GDEF marks in HarfBuzz. Using GSUB instead.
        with f.Lookup("IIb.restore_GDEF_mark_advances") as lookup:
            lookup.sub("masculine").by("_masculine")

    with builder.File(directory / "lookups-test.fea") as f:

        origin_to_alts = dict[Identity, tuple[tuple[Identity, ...], tuple[str, ...]]]()
        for name, letter in mongolian.characters.items():
            if name not in mongolian.categorization.letter:
                continue
            for joining_form, variants in letter.variants_by_joining_form.items():
                for variant in variants:
                    origin = mong(name, variant.written_units, joining_form)
                    written_unit_parts = tuple(
                        mong(written_unit, None, sliced_joining_form)
                        for written_unit, sliced_joining_form in zip(
                            variant.written_units,
                            slice_joining_form(joining_form, len(variant.written_units)),
                        )
                    )
                    pua_parts = tuple(
                        f":pua{mongolian.written_units[written_unit].variant_by_joining_form[sliced_joining_form].menksoft_pua:04X}"
                        for written_unit, sliced_joining_form in zip(
                            variant.written_units,
                            slice_joining_form(joining_form, len(variant.written_units)),
                        )
                    )
                    origin_to_alts[origin] = written_unit_parts, pua_parts

        with f.Lookup("test.ss01.wipe_phonetic_information") as lookup:
            for origin, (written_unit_parts, _) in origin_to_alts.items():
                lookup.sub(origin).by(*written_unit_parts)

        with f.Lookup("test.ss02.menksoft_pua") as lookup:
            for origin, (_, pua_parts) in origin_to_alts.items():
                lookup.sub(origin).by(*pua_parts)

    with builder.File(path) as f:

        f.include("classes-letters.fea")
        f.include("classes-categories.fea")

        with f.Table("GDEF") as table:
            table.glyph_class_definition(
                bases=None,
                ligatures=None,
                marks=[  # Somehow cannot restore advance in dist.
                    *format_control.joining_control, *format_control.fvs, "nil", "masculine",
                ],
                components=None,
            )

        f.language_system(mongolian.otl_tags()[0])

        with f.Feature("ccmp") as feature:
            with feature.Lookup("Ia.unification") as lookup:
                lookup.sub("k2").by("k")

        f.include("lookups-joining.fea")

        for name in otl.Lookup.namespace.keys():
            stage, _, joining_form_feature_tag = name.partition(".")
            if stage == "IIa":
                with f.Feature(joining_form_feature_tag) as feature:
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
