from reportlab.pdfbase import pdfmetrics
#添加中文支持
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('times', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Deng', 'Dengb.ttf'))

# pdfmetrics.registerFont(TTFont('song', 'SURSONG.TTF'))
from reportlab.graphics import barcode
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing, String, Rect
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
from reportlab.lib import units, colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.renderbase import renderScaledDrawing
from reportlab.pdfgen.canvas import Canvas
from reportlab import rl_config
 
def transform(bc, width, height):
    x1, y1, x2, y2 = bc.getBounds()
    w = float(x2 - x1)
    h = float(y2 - y1)
    sx = width not in ('auto',None)
    sy = height not in ('auto',None)
    if sx or sy:
        sx = sx and width/w or 1.0
        sy = sy and height/h or 1.0
        w *= sx
        h *= sy
    else:
        sx = sy = 1

    bc.y = 300 / sy


    d = Drawing(width=w,height=h + 300,transform=[sx,0,0,sy,-sx*x1,-sy*y1])
    d.add(bc, "_bc")
    return d

# def getTextWidth(text):

def get_barcode(value, batch = "", barWidth = 0.05 * units.inch, fontSize = 30, height = 1000, width = 3000, humanReadable = True):
    # barcode = createBarcodeDrawing('Code128', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)
    barcode = createBarcodeDrawing('Code128', height=height, width=width, value = value, barWidth = 50, humanReadable = humanReadable)
    barcode = transform(barcode.contents[0], width, height)
    drawing = Drawing(width, height + 600)

    if batch != "": 
        batch_width = stringWidth(batch, "Deng", int(fontSize*0.5))
        batch_text = String(width - batch_width - 200, 2200, batch, fontName="Deng", fontSize=int(fontSize*0.5))
        drawing.add(batch_text, "_batch")

    drawing.add(barcode, name='barcode')
    text_width = stringWidth(value, "Deng", fontSize)

    text = String((width - text_width) / 2, 50, value, fontName="Deng", fontSize=fontSize)
    drawing.add(text, "_text")
    return drawing

def drawToFile(d, c):
    """Makes a one-page PDF with just the drawing.
    If autoSize=1, the PDF will be the same size as
    the drawing; if 0, it will place the drawing on
    an A4 page with a title above it - possibly overflowing
    if too big."""

    d = renderScaledDrawing(d)

    c.setPageSize((d.width, d.height))
    renderPDF.draw(d, c, 0, 0, showBoundary=rl_config._unset_)

    c.showPage()

def getCanvas(codes, path, filename, batch_number):
    import os
    print(os.path.join(path, filename))
    c = Canvas(os.path.join(path, filename))
    for line in codes:
        line = line.strip()
        barcode = get_barcode(value = line, batch = batch_number, fontSize = 300, height = 1800, width = 4000, humanReadable=False)
        drawToFile(barcode, c)
    return c

# with open("input.txt", "r") as f:
#     c = Canvas("output.pdf")
#     c.setTitle("barcode")
#     for line in f.readlines():
#         line = line.strip()
#         barcode = get_barcode(value = line, fontSize = 300, height = 2000, width = 4000, humanReadable=False)
        
#         # renderPM.drawToString(barcode, fmt = 'png')
#         f = f'{line}.pdf'
#         # renderPM.drawToFile(barcode,fn=f,fmt='png')
#         drawToFile(barcode, c)
#     c.save()
