from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.conditions import Center2Center, Middle2Middle
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color

W, H = pt(500, 400)
doc = Document(w=W, h=H, autoPages=1)
page = doc[1]

# Create a new rectangle element with position conditions
newRect(parent=page, fill=color('red'), size=pt(240, 140),
    # Show measure lines on the element.
    showDimensions=True,
    conditions=[Center2Center(), Middle2Middle()])
# Make the page apply all conditions.
page.solve()
# Export the document page as png, so it shows as web image.
doc.export('_export/RedSquare.png')

# from typing import List

# import drawBot
# from drawBot.context.baseContext import FormattedString
# from pathlib import Path

# import pagebotosx

# directory = Path(__file__).parent

# bot = drawBot


# class CustomizedFormattedString(FormattedString):

#     def _append_positional_form(
#         self,
#         base: List[str],
#         position: str,
#     ):

#         if position in ("medi", "fina"):
#             self.cmykFill(1, 0, 0, 0)
#             self.appendGlyph("U180A")

#         self.cmykFill(0, 0, 0, 1)
#         self.appendGlyph(*base)

#         if position in ("init", "medi"):
#             self.cmykFill(1, 0, 0, 0)
#             self.appendGlyph("U180A")


# bot.newDrawing()

# bot.size("A4")  # 595, 842

# s = CustomizedFormattedString()

# s.font("Menk-Vran-Tig")
# s.fontSize(16)

# s._append_positional_form(["U1822_MED2"], "medi")

# x = 20
# y = bot.height() - 20

# # rotate(90)

# bot.text(s, (x, y))

# bot.saveImage((directory / "chart.pdf").as_posix())

# bot.endDrawing()
