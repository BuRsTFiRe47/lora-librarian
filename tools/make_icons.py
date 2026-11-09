# -*- coding: utf-8 -*-
"""
Generates the app icon (PNG / ICO / ICNS + embedded icon_data.py) for the
chosen app, drawn with Qt so it stays crisp and needs no image editor.

    python tools/make_icons.py            # run from the repo root

Uygulama ikonunu (PNG / ICO / ICNS + gömülü icon_data.py) Qt ile çizer.
"""
import base64, io, os, sys
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (QGuiApplication, QImage, QPainter, QColor, QLinearGradient, QPainterPath,
                           QPen, QBrush, QPolygonF)
from PIL import Image

APP = "lora-librarian"      # <- "lora-librarian" or "preview-smith"
S = 1024

BG_TOP, BG_BOT = QColor("#2a2b44"), QColor("#13131f")
EDGE = QColor(255, 255, 255, 34)
CORAL, CORAL_HI = QColor("#e0555a"), QColor("#ff7a78")
OFFWHITE, STEEL = QColor("#eceef7"), QColor("#8a93b8")


def tile(p):
    r = QRectF(40, 40, S - 80, S - 80)
    g = QLinearGradient(0, r.top(), 0, r.bottom())
    g.setColorAt(0, BG_TOP); g.setColorAt(1, BG_BOT)
    p.setPen(Qt.NoPen); p.setBrush(QBrush(g))
    p.drawRoundedRect(r, 210, 210)
    p.setPen(QPen(EDGE, 6)); p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(r.adjusted(5, 5, -5, -5), 205, 205)


def rounded_top_rect(x, y, w, h, rt, rb=14):
    path = QPainterPath()
    path.moveTo(x, y + h - rb)
    path.lineTo(x, y + rt)
    path.quadTo(x, y, x + rt, y)
    path.lineTo(x + w - rt, y)
    path.quadTo(x + w, y, x + w, y + rt)
    path.lineTo(x + w, y + h - rb)
    path.quadTo(x + w, y + h, x + w - rb, y + h)
    path.lineTo(x + rb, y + h)
    path.quadTo(x, y + h, x, y + h - rb)
    path.closeSubpath()
    return path


def glyph_librarian(p):
    """Three book spines on a shelf; the coral one leans in."""
    base = 730
    p.setPen(Qt.NoPen)
    # book 1 (tall, off-white) + band
    p.setBrush(OFFWHITE); p.drawPath(rounded_top_rect(235, 290, 150, base - 290, 28))
    p.setBrush(STEEL); p.drawRect(QRectF(235, 360, 150, 26)); p.drawRect(QRectF(235, 640, 150, 18))
    # book 2 (medium, steel)
    p.setBrush(STEEL); p.drawPath(rounded_top_rect(415, 360, 150, base - 360, 28))
    p.setBrush(OFFWHITE); p.drawRect(QRectF(415, 430, 150, 26)); p.drawRect(QRectF(415, 640, 150, 18))
    # book 3 (leaning, coral)
    p.save()
    p.translate(805, base); p.rotate(14); p.translate(-805, -base)
    g = QLinearGradient(0, 300, 0, base); g.setColorAt(0, CORAL_HI); g.setColorAt(1, CORAL)
    p.setBrush(QBrush(g)); p.drawPath(rounded_top_rect(600, 300, 150, base - 300, 28))
    p.setBrush(QColor(255, 255, 255, 215)); p.drawRect(QRectF(600, 372, 150, 26)); p.drawRect(QRectF(600, 640, 150, 18))
    p.restore()
    # shelf
    p.setBrush(QColor(255, 255, 255, 235)); p.drawRoundedRect(QRectF(190, base + 8, 644, 34), 17, 17)


def glyph_smith(p):
    """Film frame with a coral play button and forge sparks."""
    p.setPen(Qt.NoPen)
    frame = QRectF(205, 300, 614, 424)
    p.setBrush(OFFWHITE); p.drawRoundedRect(frame, 56, 56)
    p.setBrush(QColor("#1b1c2e")); p.drawRoundedRect(frame.adjusted(46, 46, -46, -46), 30, 30)
    # sprocket holes along both edges
    p.setBrush(QColor("#1b1c2e"))
    for i in range(4):
        y = 338 + i * 92
        p.drawRoundedRect(QRectF(frame.left() + 12, y, 22, 40), 7, 7)
        p.drawRoundedRect(QRectF(frame.right() - 34, y, 22, 40), 7, 7)
    # play triangle
    cx, cy = 512, 512
    tri = QPolygonF([QPointF(cx - 70, cy - 105), QPointF(cx - 70, cy + 105), QPointF(cx + 112, cy)])
    g = QLinearGradient(0, cy - 105, 0, cy + 105); g.setColorAt(0, CORAL_HI); g.setColorAt(1, CORAL)
    p.setBrush(QBrush(g))
    p.setPen(QPen(QBrush(g), 36, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    p.drawPolygon(tri)
    # sparks
    p.setPen(Qt.NoPen)
    for (x, y, r, a) in [(790, 250, 22, 255), (850, 190, 14, 220), (720, 190, 11, 200)]:
        p.setBrush(QColor(255, 190, 120, a)); p.drawEllipse(QPointF(x, y), r, r)
    star = QPainterPath()
    cxs, cys, rr = 800, 250, 52
    star.moveTo(cxs, cys - rr); star.quadTo(cxs, cys, cxs + rr, cys); star.quadTo(cxs, cys, cxs, cys + rr)
    star.quadTo(cxs, cys, cxs - rr, cys); star.quadTo(cxs, cys, cxs, cys - rr)
    p.setBrush(QColor("#ffd29a")); p.drawPath(star)


def render():
    img = QImage(S, S, QImage.Format_ARGB32)
    img.fill(Qt.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.SmoothPixmapTransform)
    tile(p)
    (glyph_librarian if APP == "lora-librarian" else glyph_smith)(p)
    p.end()
    return img


def main():
    QGuiApplication(sys.argv)
    out = os.path.join(os.getcwd(), "assets")
    os.makedirs(out, exist_ok=True)
    big = "/tmp/_icon_big.png"
    render().save(big)
    im = Image.open(big).convert("RGBA")
    im512 = im.resize((512, 512), Image.LANCZOS)
    im512.save(os.path.join(out, "icon.png"))
    im.save(os.path.join(out, "icon.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    im.save(os.path.join(out, "icon.icns"), sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)])
    # embedded copy: works in a PyInstaller bundle without data-file plumbing
    buf = io.BytesIO(); im.resize((256, 256), Image.LANCZOS).save(buf, "PNG", optimize=True)
    with open("icon_data.py", "w", encoding="utf-8") as f:
        f.write('# -*- coding: utf-8 -*-\n# Generated by tools/make_icons.py - do not edit.\nICON_PNG_B64 = (\n')
        b = base64.b64encode(buf.getvalue()).decode()
        for i in range(0, len(b), 100):
            f.write(f'    "{b[i:i+100]}"\n')
        f.write(')\n')
    print("icons written to", out)


if __name__ == "__main__":
    main()
