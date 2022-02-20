from pathlib import Path

import uharfbuzz as hb


class Shaper:
    def __init__(self, path: Path):
        face = hb.Face(path.read_bytes())  # type: ignore
        self.font = hb.Font(face)  # type: ignore
        hb.ot_font_set_funcs(self.font)  # type: ignore

    def shape_text_to_glyph_names(
        self,
        text: str,
        features: dict = None,
        gid_to_name: dict[int, str] = None,
    ) -> list[str]:

        buffer = hb.Buffer()  # type: ignore
        buffer.add_str(text)
        buffer.guess_segment_properties()

        hb.shape(self.font, buffer, features)  # type: ignore

        names = list[str]()
        for info, position in zip(buffer.glyph_infos, buffer.glyph_positions or []):
            gid = info.codepoint
            if gid_to_name is None:
                name = self.font.get_glyph_name(gid)
            else:
                name = gid_to_name.get(gid, f"gid{gid}")
            if (
                name == "space" and position.x_advance == 0
            ):  # HarfBuzz pseudo space for invisible glyphs
                name = "_invisible"
            names.append(name)

        return names
