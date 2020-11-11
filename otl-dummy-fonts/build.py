import functools
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import yaml
from tptqscripttools.data import REGISTER
from tptqscripttools.objects import DevelopmentNaming, Script
from tptqscripttools.otl import DEFAULT_LANGUAGE_TAG, FeaFile, GlyphSpace

scripting_path = Path(__file__)
project_dir = scripting_path.parent

data_dir = project_dir / ".." / "utn" / "data"
otl_dir = project_dir / "stateless"
product_dir = project_dir / "products"

class SimpleNaming(DevelopmentNaming):
    make_name = functools.partial(
        DevelopmentNaming.make_name, implied_script_codes = [Script.COMMON_CODE, "Mong"],
    )

data = SimpleNamespace()


def main():

    glyph_naming_scheme = SimpleNaming

    for filename in ["written-units", "characters", "categories"]:
        text = (data_dir / filename).with_suffix(".yaml").read_text()
        data.__dict__[filename.replace("-", "_")] = make_namespace(yaml.safe_load(text))

    script = REGISTER.script_by_code["Mong"]
    glyph_space = script.glyph_space(source=None, naming=glyph_naming_scheme)  # not checking availability in a source glyph set

    otl_path = make_otl_file(glyph_space)
    script.export_otl_dummy_font(
        project_dir / "products", naming=glyph_naming_scheme, feature_file_path=otl_path,
    )


def make_otl_file(glyph_space: GlyphSpace) -> Path:

    mong = glyph_space

    classes = SimpleNamespace()
    lookups = SimpleNamespace()

    with FeaFile(otl_dir / "classes.fea", source=scripting_path) as file:

        for name in data.categories.letter:
            classes.__dict__[name] = []
            letter = data.characters.__dict__[name]
            for joining_form, variants in letter.joining_form_to_variants.__dict__.items():
                class_name = "@" + name + "." + joining_form
                file.classDefinition(class_name, [
                    mong[name + "." + "".join(v.written_units) + "." + joining_form]
                    for v in variants
                ])
                classes.__dict__[name].append(class_name)

        for name in data.categories.letter:
            class_name = "@" + name
            file.classDefinition(class_name, classes.__dict__[name])

        for categoty in ["vowel", "masculine", "feminine", "neuter", "consonant"]:
            file.classDefinition("@" + categoty, ["@" + name for name in data.categories.__dict__[categoty]])

    with FeaFile(otl_dir / "lookups.fea", source=scripting_path) as file:

        lookups.IIa = []
        for joining_form in ["isol", "init", "medi", "fina"]:
            lookup_name = "IIa." + joining_form
            with file.Lookup(lookup_name) as lookup:
                for name in data.categories.letter:
                    lookup.substitution(mong[name], mong[name + "." + joining_form])
            lookups.IIa.append(lookup_name)

    with FeaFile(otl_dir / "main.fea", source=scripting_path) as file:

        # file.raw("include(classes.fea);")

        file.raw([
            "table GDEF {",  # Bases, ligatures, marks, components
            "    GlyphClassDef , , [{}], ;".format(
                " ".join(mong[name] for name in data.categories.joining_control + data.categories.fvs)
            ),
            "} GDEF;",
        ])

        # file.languageSystem(mong.script.info.otl.tags[0], DEFAULT_LANGUAGE_TAG)

        # file.raw("include(lookups.fea);")

        for joining_form in ["isol", "init", "medi", "fina"]:
            feature = file.feature(joining_form)
            feature.lookupReference(
                next(name for name in lookups.IIa if name.endswith(joining_form))
            )

    # feaLib’s include() following somehow fails.
    stitched_otl_path = otl_dir / "stateless.fea"
    with stitched_otl_path.open("w") as f:
        for filename in ["classes.fea", "lookups.fea", "main.fea"]:
            f.write((otl_dir / filename).read_text())

    return stitched_otl_path


def make_namespace(content: Any) -> Any:
    if isinstance(content, dict):
        return SimpleNamespace(**{k: make_namespace(v) for k, v in content.items()})
    elif isinstance(content, list):
        if content and isinstance(i := content[0], dict) and "ascii_transcription" in i.keys():
            return SimpleNamespace(**{
                make_namespace(i["ascii_transcription"]): make_namespace(i) for i in content
            })
        else:
            return [make_namespace(i) for i in content]
    elif isinstance(content, str):
        return {"zwnj": ":zero-width-non-joiner", "zwj": ":zero-width-joiner"}.get(content, content)
    else:
        return content


if __name__ == "__main__":
    main()
