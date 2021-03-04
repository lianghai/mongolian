import difflib
from pathlib import Path

from tptqutils.shaping import Shaper

from data import Mongolian as Mong
from data import glyph_set
from utils import slice_joining_form

scripting_dir = Path(__file__).parent
project_dir = scripting_dir / ".."
repo_dir = scripting_dir / ".." / ".."
private_repo_dir = repo_dir / ".." / "mongolian-private"
font_dir = private_repo_dir / "misc/liangjinbao/20210303"

cp_to_name = {chr(character.cp): character_id for character_id, character in Mong.characters.items()}

def main():

    for test_case in [
        "ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ",
        "ᠥᠪᠡᠷᠲᠡᠭᠡᠨ ᠵᠠᠰᠠᠬᠤ ᠣᠷᠣᠨ",
        "ᠠᠲᠠ",
    ]:

        eac_shaper = Shaper(font_dir / "NotoSansMongolian-Regular.ttf")
        eac_result = normalized(eac_shaper.shape_text_to_glyph_names(test_case))

        utn_shaper = Shaper(project_dir / "products" / "DummyStateless-Regular.otf")
        utn_result = normalized(utn_shaper.shape_text_to_glyph_names(test_case))

        print(*(cp_to_name.get(i) or i for i in test_case))
        if eac_result == utn_result:
            print("pass")
        else:
            for line in difflib.unified_diff(eac_result, utn_result):
                print(line)
            # print(*eac_result)
            # print(*utn_result)
        print()

    # for name in glyph_set:
    #     body, *suffixes = name.split(".")
    #     if body.startswith(("uni", "u")):
    #         print(name, [cp_to_name.get(chr(int(i, 16))) for i in body.removeprefix("uni").removeprefix("u").split("_")])

mapping = {

    "u182E.ini": "m.M.init",
    "u1823.med": "o.O.medi",
    "u1829.med": "ng.A_G.medi",
    "u182D.medV1": "g.Gh.medi",
    "u1823.med": "o.O.medi",
    "u182F.fin": "l.L.fina",

    "u182A_1822.ini": "b_i.B_I.init",
    "u1834.med": "ch.Ch.medi",
    "u1822.medFem": "i.I.medi",
    "u182D.finV1": "g.G.fina",

    "u1825.ini": "oe.A_O_I.init",
    "u182A_1821.med": "b_e.B_A.medi",
    "u1837.med": "r.R.medi",
    "u1832.med": "t.D.medi",
    "u1821.med": "e.A.medi",
    "u182D_1821.med": "g_e.G_A.medi",
    "u1828.fin": "n.A.fina",

    "u1835.ini": "j.I.init",
    "u1820.med": "a.A.medi",
    "u1830.med": "s.S.medi",
    "u1820.med": "a.A.medi",
    "u182C.med": "h.H.medi",
    "u1824.fin": "u.U.fina",

    "u1823.ini": "o.A_O.init",
    "u1837.med": "r.R.medi",
    "u1823.med": "o.O.medi",
    "u1828.fin": "n.A.fina",

    "u1820.ini": "a.A_A.init",
    "u1820.fin": "a.A.fina",
}

def normalized(names: list[str]) -> list[str]:
    normalized_names = []
    for name in (mapping.get(i) or i for i in names):
        name_elements = name.split(".")
        if not len(name_elements) == 3:
            normalized_names.append(name)
            continue
        _, graphic, joining_form = name_elements
        graphic_parts = graphic.split("_")
        joining_forms = slice_joining_form(joining_form, len(graphic_parts))
        normalized_names.extend(
            ".".join(i) for i in zip(graphic_parts, joining_forms)
        )
    return normalized_names


if __name__ == "__main__":
    main()
