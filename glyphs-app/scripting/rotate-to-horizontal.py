# encoding: UTF-8
# MenuTitle: Rotate text orientation from vertical (↓) to horizontal (→)
# Author: 梁海 Liang Hai
# Date: 29 Mar 2020

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from mongolian_scripting import transform_font, V_TO_H


def main():
    font = Glyphs.font
    font.disableUpdateInterface()
    transform_font(font, V_TO_H)
    font.enableUpdateInterface()


if __name__ == "__main__":
    main()
