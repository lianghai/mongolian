# encoding: UTF-8
# MenuTitle: Export instances
# Author: 梁海 Liang Hai
# Date: 29 Mar 2020

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from mongolian_scripting import transform_font, V_TO_H


def main():
    temp_font = Glyphs.font.copy()
    transform_font(temp_font, V_TO_H)
    Glyphs.showMacroWindow()
    for instance in temp_font.instances:
        if not instance.active:
            continue
        result = instance.generate(
            # Format=,
            # FontPath=,
            AutoHint=False,
            RemoveOverlap=False,
            UseSubroutines=False,
            UseProductionNames=False,
            # Containers=,
        )
        if result is True:
            print("Exported instance: {}".format(instance.name))
        else:
            print(result)

if __name__ == "__main__":
    main()
