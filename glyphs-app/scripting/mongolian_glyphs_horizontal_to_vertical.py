# encoding: UTF-8
# MenuTitle: 蒙文字体图形横改竖
# Liang Hai, 20 Oct 2018

from __future__ import division, absolute_import, print_function, unicode_literals

font = Glyphs.font

font.disableUpdateInterface()

for g in font.glyphs:

    left_key = g.leftMetricsKey
    width_key = g.widthMetricsKey
    right_key = g.rightMetricsKey
    top_key = g.topMetricsKey()
    height_key = g.vertWidthMetricsKey()
    bottom_key = g.bottomMetricsKey()

    g.leftMetricsKey = bottom_key
    g.widthMetricsKey = height_key
    g.rightMetricsKey = top_key
    g.setTopMetricsKey_(left_key)
    g.setVertWidthMetricsKey_(width_key)
    g.setBottomMetricsKey_(right_key)

    for l in g.layers:

        transform = NSAffineTransform.transform()
        transform.rotateByDegrees_(-90.0)

        master = font.masters[l.associatedMasterId]
        ascender = master.ascender
        descender = master.descender
        transform.translateXBy_yBy_(-ascender, -descender)

        l.transform_checkForSelection_doComponents_(transform, False, False)

        if l.vertWidth() == -1.0:
            l.setVertWidth_(l.vertWidthDefault())
        width = l.width
        height = l.vertWidth()
        l.width = height
        l.setVertWidth_(width)

        for c in l.components:
            x, y = c.position
            c.position = NSPoint(y, -x)

font.enableUpdateInterface()
