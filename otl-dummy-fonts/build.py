from pathlib import Path

from tptqscripttools.data import REGISTER
from tptqscripttools.objects import Script
from tptqscripttools.otl import FeaFile

scripting_path = Path(__file__)
project_dir = scripting_path.parent

feature_file_path = project_dir / "stateless.fea"
product_dir = project_dir / "products"


def main():
    script = REGISTER.script_by_code["Mong"]
    glyph_space = script.glyph_space()  # not checking availability in a source glyph set
    build_otl_feature_file(glyph_space)
    script.export_otl_dummy_font(project_dir / "products", feature_file_path)


def build_otl_feature_file(glyph_space: Script):

    mong = glyph_space

    with FeaFile(feature_file_path, source=scripting_path) as file:
        pass


if __name__ == "__main__":
    main()
