# encoding: UTF-8
# MenuTitle: Rotate text orientation from horizontal (→) to vertical (↓)
# Author: 梁海 Liang Hai
# Date: 29 Mar 2020 (originally experimented on 20 Oct 2018)

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from mongolian_scripting import transform_font, H_TO_V


def main():
    font = Glyphs.font
    font.disableUpdateInterface()
    transform_font(font, H_TO_V)
    font.enableUpdateInterface()


if __name__ == "__main__":
    main()
