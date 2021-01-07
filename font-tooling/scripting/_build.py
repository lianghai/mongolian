from fontmake.font_project import FontProject
import defcon
from pathlib import Path

SCRIPTING_DIR = Path(__file__).parent

INPUT_DIR = SCRIPTING_DIR / "eac"
UFO_PATH = INPUT_DIR / "variants" / "variants.ufo"
FEA_PATH = INPUT_DIR / "otl.fea"

OUTPUT_DIR = SCRIPTING_DIR / "products"
FAMILY_NAME = "Sandbox EAC"
FORMAT = "otf"

ufo = defcon.Font(path=UFO_PATH)

ufo.info.familyName = FAMILY_NAME
ufo.info.styleName = "Regular"

project = FontProject()

font_name = project._font_name(ufo)
output_path = project._output_path(font_name, FORMAT, output_dir=OUTPUT_DIR)

project.run_from_ufos(
    [ufo],
    output=[FORMAT],
    # For .save_otfs:
    remove_overlaps=False,
    output_path=output_path,
    debug_feature_file=(OUTPUT_DIR / "debug.fea").open("w")
)
