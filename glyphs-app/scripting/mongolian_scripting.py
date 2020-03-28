# Encoding: UTF-8
# Author: 梁海 Liang Hai
# Date: 29 Mar 2020


from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from Foundation import NSPoint

H_TO_V = -90.0, (0, -1.0, 1.0, 0, 0, 0)
V_TO_H =  90.0, (0, 1.0, -1.0, 0, 0, 0)


def transform_font(font, transform):

    font.disablesAutomaticAlignment = True

    for glyph in font.glyphs:
        transform_glyph(glyph, transform)

    for master in font.masters:
        for guide in master.guides:
            transform_guide(guide, transform)
        if transform is H_TO_V:
            for attribute in ["ascender", "capHeight", "xHeight", "descender"]:
                key = "io.lianghai.backup.{}".format(attribute)
                master.customParameters[key] = getattr(master, attribute)
            master.descender -= master.ascender
            master.ascender = 0.0
            master.capHeight, master.xHeight = 0.0, 0.0
        else:
            for attribute in ["ascender", "capHeight", "xHeight", "descender"]:
                key = "io.lianghai.backup.{}".format(attribute)
                setattr(master, attribute, master.customParameters[key])
                del master.customParameters[key]

    if transform is H_TO_V:
        font.customParameters["io.lianghai.state"] =  "mongolian.ttb"
        for tab in font.tabs:
            tab.direction = LTRTTB
    else:
        del font.customParameters["io.lianghai.state"]
        try:
            for tab in font.tabs:
                tab.direction = LTR
        except AttributeError:
            pass


def transform_glyph(glyph, transform):

    g = glyph
    degrees, matrix = transform

    w_metrics_key = g.widthMetricsKey
    h_metrics_key = g.vertWidthMetricsKey()
    g.widthMetricsKey = h_metrics_key
    g.setVertWidthMetricsKey_(w_metrics_key)

    l_metrics_key = g.leftMetricsKey
    r_metrics_key = g.rightMetricsKey
    t_metrics_key = g.topMetricsKey()
    b_metrics_key = g.bottomMetricsKey()
    l_kerning_group = g.leftKerningGroup
    r_kerning_group = g.rightKerningGroup
    t_kerning_group = g.topKerningGroup()
    b_kerning_group = g.bottomKerningGroup()
    if transform is H_TO_V:
        g.leftMetricsKey = b_metrics_key
        g.rightMetricsKey = t_metrics_key
        g.setTopMetricsKey_(l_metrics_key)
        g.setBottomMetricsKey_(r_metrics_key)
        g.leftKerningGroup = b_kerning_group
        g.rightKerningGroup = t_kerning_group
        g.setTopKerningGroup_(l_kerning_group)
        g.setBottomKerningGroup_(r_kerning_group)
    else:
        g.leftMetricsKey = t_metrics_key
        g.rightMetricsKey = b_metrics_key
        g.setTopMetricsKey_(r_metrics_key)
        g.setBottomMetricsKey_(l_metrics_key)
        g.leftKerningGroup = t_kerning_group
        g.rightKerningGroup = b_kerning_group
        g.setTopKerningGroup_(r_kerning_group)
        g.setBottomKerningGroup_(l_kerning_group)

    for l in g.layers:
        l.applyTransform(matrix)
        for c in l.components:
            c.rotation = c.rotation - degrees
        for guide in l.guides:
            transform_guide(guide, transform)
        if transform is H_TO_V:
            l.vertOrigin = 0.0
            l.vertWidth = l.width
            l.width = g.parent.masters[l.associatedMasterId].ascender
        else:
            l.width = l.vertWidth
            l.vertOrigin = None
            l.vertWidth = None
        l.setNeedUpdateMetrics()


def transform_guide(guide, transform):
    degrees, matrix = transform
    guide.angle += degrees
    if transform is H_TO_V:
        guide.position = NSPoint(guide.position.y, -guide.position.x)
    else:
        guide.position = NSPoint(-guide.position.y, guide.position.x)
