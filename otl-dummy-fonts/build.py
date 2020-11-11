from pathlib import Path
from types import SimpleNamespace
from typing import Any

import yaml
from tptqscripttools.data import REGISTER
from tptqscripttools.otl import FeaFile

scripting_path = Path(__file__)
project_dir = scripting_path.parent

feature_file_path = project_dir / "stateless.fea"
product_dir = project_dir / "products"

def make_namespace(content: Any) -> Any:
    if isinstance(content, dict):
        return SimpleNamespace(**{k: make_namespace(v) for k, v in content.items()})
    elif isinstance(content, list):
        if content and isinstance(i := content[0], dict) and "ascii_transcription" in i.keys():
            return SimpleNamespace(**{i["ascii_transcription"]: make_namespace(i) for i in content})
        else:
            return [make_namespace(i) for i in content]
    else:
        return content

data_dir = project_dir / ".." / "utn" / "data"
data_dict = {}
for filename in ["written-units", "characters", "syllabic-category"]:
    text = (data_dir / filename).with_suffix(".yaml").read_text()
    data_dict[filename.replace("-", "_")] = make_namespace(yaml.safe_load(text))
data = SimpleNamespace(**data_dict)


def main():

    script = REGISTER.script_by_code["Mong"]
    mong = script.glyph_space()  # not checking availability in a source glyph set

    with FeaFile(feature_file_path, source=scripting_path) as file:

        vowel_subclass_to_members = {
            "masculine": ["a", "o", "u"],
            "feminine": ["e", "oe", "ue", "eh"],
            "neuter": ["i"],
        }
        for subclass, members in vowel_subclass_to_members.items():
            file.classDefinition("@vowel." + subclass, ["@" + m for m in members])
        file.classDefinition("@vowel", ["@vowel." + s for s in vowel_subclass_to_members.keys()])

    return

    script.export_otl_dummy_font(project_dir / "products", feature_file_path)


if __name__ == "__main__":
    main()
