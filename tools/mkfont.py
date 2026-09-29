"""Noto Sans CJK KR(CFF) -> 보고서에 쓰인 글자만 부분집합으로 잘라 TrueType(glyf)으로 변환한다.
reportlab이 CFF 윤곽선을 못 읽기 때문. 결과: /tmp/fonts/K-Regular.ttf, K-Bold.ttf"""
import os, sys
from fontTools.ttLib import TTCollection, TTFont, newTable
from fontTools import subset
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

src = open(os.path.join(os.path.dirname(__file__), "build_report.py"), encoding="utf-8").read()
chars = set(src) | set("0123456789.,%()[]{}<>=+-*/×÷≈≥≤→←↔·○◎△✕①②③④⑤⑥ⓐ※“”‘’ ") | {chr(c) for c in range(32, 127)}
text = "".join(sorted(chars))

def convert(ttc, out):
    coll = TTCollection(ttc)
    font = next(f for f in coll.fonts if "KR" in f["name"].getDebugName(1))
    opts = subset.Options(); opts.layout_features = ["*"]; opts.notdef_outline = True
    sub = subset.Subsetter(opts); sub.populate(text=text); sub.subset(font)
    glyphOrder = font.getGlyphOrder(); gs = font.getGlyphSet()
    glyf = newTable("glyf"); glyf.glyphOrder = glyphOrder; glyf.glyphs = {}
    for name in glyphOrder:
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyf.glyphs[name] = pen.glyph()
    font["glyf"] = glyf; font["loca"] = newTable("loca")
    maxp = font["maxp"]; maxp.tableVersion = 0x00010000
    for a in ("maxZones","maxTwilightPoints","maxStorage","maxFunctionDefs","maxInstructionDefs","maxStackElements","maxSizeOfInstructions","maxComponentElements"):
        setattr(maxp, a, 0)
    maxp.maxZones = 1; maxp.maxPoints = maxp.maxContours = maxp.maxCompositePoints = maxp.maxCompositeContours = 0
    maxp.maxComponentDepth = 0
    post = font["post"]; post.formatType = 2.0; post.extraNames = []; post.mapping = {}; post.glyphOrder = glyphOrder
    del font["CFF "]
    if "VORG" in font: del font["VORG"]
    font["head"].glyphDataFormat = 0
    font.sfntVersion = "\x00\x01\x00\x00"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    font.save(out); print("saved", out, os.path.getsize(out) // 1024, "KB")

base = "/usr/share/fonts/opentype/noto/"
convert(base + "NotoSansCJK-Regular.ttc", "/tmp/fonts/K-Regular.ttf")
convert(base + "NotoSansCJK-Bold.ttc", "/tmp/fonts/K-Bold.ttf")
