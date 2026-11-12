"""깔끔한 강의 템플릿(clean-template.pptx)을 만든다 — 로고 없음, 흰 바탕, 청록 포인트.

슬라이드 3장 + 레이아웃 3개로 구성되어 deckkit.Deck(theme="clean")이 그대로 쓴다.
  * 1번 슬라이드 = 표지        ({EVENT} {TITLE} {SUB} {AUTHOR} {DATE} 자리 표시)
  * 2번 슬라이드 = 본문 원형    (Title and Content 레이아웃 + 푸터 {FOOTER} + 쪽번호)
  * 3번 슬라이드 = 마지막(Q&A)  ({NEXT})
  * 레이아웃: "Title Slide", "Title and Content", "Section"
테마 글꼴은 맑은 고딕, 테마 색 accent1/accent2 = 청록/주황.
사용: python make_clean_template.py  → build/clean-template.pptx
"""
import copy
import os

from lxml import etree
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "clean-template.pptx")

FONT = "맑은 고딕"
TEAL, ORANGE, INK, GRAY, LINE, TINT = "01688F", "E97132", "1B2A36", "5E6B75", "C5D9E4", "EDF5F9"
SW, SH = 13.333, 7.5

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
master = prs.slide_masters[0]

# ---------------------------------------------------------------- 테마: 글꼴·색
theme_part = master.part.part_related_by(RT.THEME)
theme = etree.fromstring(theme_part.blob)
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
ns = {"a": A}
for tag in ("majorFont", "minorFont"):
    f = theme.find(f".//a:{tag}", ns)
    f.find("a:latin", ns).set("typeface", FONT)
    f.find("a:ea", ns).set("typeface", FONT)
for name, val in {"dk2": INK, "accent1": TEAL, "accent2": ORANGE, "accent3": "00A3CA", "accent4": "72ABC8"}.items():
    el = theme.find(f".//a:clrScheme/a:{name}", ns)
    for c in list(el):
        el.remove(c)
    etree.SubElement(el, f"{{{A}}}srgbClr", val=val)
theme.find(".//a:clrScheme", ns).set("name", "AI Zero 2 Transformer")
for es in theme.findall(".//a:effectStyleLst/a:effectStyle", ns):  # 그림자·입체 효과 없음
    for c in list(es):
        es.remove(c)
    etree.SubElement(es, f"{{{A}}}effectLst")
theme.find(".//a:fontScheme", ns).set("name", "AI Zero 2 Transformer")
theme_part._blob = etree.tostring(theme, xml_declaration=True, encoding="UTF-8", standalone=True)


def rgb_el(parent, hexv):
    sf = etree.SubElement(parent, qn("a:solidFill"))
    etree.SubElement(sf, qn("a:srgbClr"), val=hexv)


def set_run(run, size, color, bold=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = __import__("pptx").dml.color.RGBColor.from_string(color)
    run.font.name = FONT
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", FONT)


def place(ph, x, y, w, h):
    ph.left, ph.top, ph.width, ph.height = Inches(x), Inches(y), Inches(w), Inches(h)


def lst_style(ph, size, color, bold=False, align=None, anchor=None):
    """레이아웃 개체 틀의 기본 글자 모양(lstStyle lvl1)을 지정."""
    txBody = ph._element.find(qn("p:txBody"))
    old = txBody.find(qn("a:lstStyle"))
    new = etree.Element(qn("a:lstStyle"))
    lvl = etree.SubElement(new, qn("a:lvl1pPr"), marL="0", indent="0")
    if align:
        lvl.set("algn", align)
    etree.SubElement(lvl, qn("a:buNone"))
    d = etree.SubElement(lvl, qn("a:defRPr"), sz=str(int(size * 100)), b="1" if bold else "0")
    rgb_el(d, color)
    etree.SubElement(d, qn("a:latin"), typeface="+mj-lt" if bold else "+mn-lt")
    etree.SubElement(d, qn("a:ea"), typeface="+mj-ea" if bold else "+mn-ea")
    txBody.replace(old, new)
    if anchor:
        txBody.find(qn("a:bodyPr")).set("anchor", anchor)


def add_rect(shapes, x, y, w, h, color, line=None):
    s = shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = __import__("pptx").dml.color.RGBColor.from_string(color)
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def add_line(shapes, x1, y, x2, color, width):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y), Inches(x2), Inches(y))
    c.line.color.rgb = __import__("pptx").dml.color.RGBColor.from_string(color)
    c.line.width = Pt(width)
    return c


def add_text(shapes, text, x, y, w, h, size, color, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for k in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, k, 0)
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        set_run(p.add_run(), size, color, bold)
        p.runs[0].text = line
    return tb


def on_layout(layout, draw):
    """레이아웃 도형은 python-pptx에서 직접 추가할 수 없어, 임시 슬라이드에 그린 뒤 XML을 옮긴다."""
    tmp = prs.slides.add_slide(layout)
    for ph in list(tmp.placeholders):
        ph._element.getparent().remove(ph._element)
    draw(tmp.shapes)
    tree = layout.shapes._spTree
    for el in list(tmp.shapes._spTree)[2:]:
        tree.append(el)
    lst = prs.slides._sldIdLst
    sid = list(lst)[-1]
    prs.part.drop_rel(sid.get(qn("r:id")))
    lst.remove(sid)


def drop_layout(layout):
    lst = master._element.find(qn("p:sldLayoutIdLst"))
    for el in list(lst):
        if master.part.related_part(el.get(qn("r:id"))) is layout.part:
            master.part.drop_rel(el.get(qn("r:id")))
            lst.remove(el)


# ---------------------------------------------------------------- 마스터: 16:9 위치 · 기본 글꼴
for ph in master.placeholders:
    t = ph.placeholder_format.type
    name = str(t)
    if "TITLE" in name:
        place(ph, 0.5, 0.22, 12.33, 0.62)
    elif "BODY" in name:
        place(ph, 0.5, 1.2, 12.33, 5.6)
    elif "SLIDE_NUMBER" in name:
        place(ph, 11.83, 7.05, 1.0, 0.3)
    elif "DATE" in name:
        place(ph, 0.5, 7.05, 3.0, 0.3)
    elif "FOOTER" in name:
        place(ph, 4.0, 7.05, 5.3, 0.3)
tx = master._element.find(qn("p:txStyles"))
for d in tx.iter(qn("a:defRPr")):
    for c in list(d):
        if c.tag in (qn("a:solidFill"),):
            d.remove(c)
title_lvl = tx.find(qn("p:titleStyle")).find(qn("a:lvl1pPr"))
title_lvl.find(qn("a:defRPr")).set("sz", "2800")
title_lvl.find(qn("a:defRPr")).set("b", "1")
rgb_el(title_lvl.find(qn("a:defRPr")), INK)
for lvl in tx.find(qn("p:bodyStyle")):
    d = lvl.find(qn("a:defRPr"))
    if d is not None:
        rgb_el(d, INK)

layouts = {l.name: l for l in master.slide_layouts}
L_TITLE, L_CONTENT, L_SECTION = layouts["Title Slide"], layouts["Title and Content"], layouts["Section Header"]
for name, l in layouts.items():
    if l not in (L_TITLE, L_CONTENT, L_SECTION):
        drop_layout(l)
L_SECTION.name = "Section"

# ---------------------------------------------------------------- 레이아웃: 본문 (Title and Content)
for ph in list(L_CONTENT.placeholders):
    t = str(ph.placeholder_format.type)
    if "TITLE" in t:
        place(ph, 0.5, 0.22, 12.33, 0.62)
        lst_style(ph, 28, INK, bold=True, align="l", anchor="b")
        ph._element.find(qn("p:txBody")).find(qn("a:bodyPr")).set("lIns", "0")
    elif "BODY" in t or "OBJECT" in t:
        place(ph, 0.5, 1.2, 12.33, 5.6)
    elif "SLIDE_NUMBER" in t:
        place(ph, 11.83, 7.05, 1.0, 0.3)
        lst_style(ph, 10, GRAY, align="r", anchor="ctr")
    else:  # 날짜·바닥글 개체 틀은 쓰지 않는다
        ph._element.getparent().remove(ph._element)
on_layout(L_CONTENT, lambda sh: (add_line(sh, 0.5, 0.86, 12.83, LINE, 1.0), add_line(sh, 0.5, 0.86, 1.4, TEAL, 3.0)))

# ---------------------------------------------------------------- 레이아웃: 구역 (Section)
on_layout(L_SECTION, lambda sh: (add_rect(sh, 0, 0, 0.25, SH, TEAL), add_rect(sh, 1.0, 4.0, 1.2, 0.07, ORANGE)))
for ph in list(L_SECTION.placeholders):
    t = str(ph.placeholder_format.type)
    if "TITLE" in t:
        place(ph, 1.0, 1.9, 11.3, 1.95)
        lst_style(ph, 36, INK, bold=True, align="l", anchor="b")
    elif "BODY" in t:
        place(ph, 1.0, 4.3, 11.3, 1.4)
        lst_style(ph, 20, GRAY, align="l", anchor="t")
    else:
        ph._element.getparent().remove(ph._element)

# ---------------------------------------------------------------- 레이아웃: 표지 (Title Slide) — 자리 표시는 슬라이드의 글상자로
for ph in list(L_TITLE.placeholders):
    ph._element.getparent().remove(ph._element)
on_layout(L_TITLE, lambda sh: add_rect(sh, 0, 0, 0.25, SH, TEAL))

# 장식 도형이 개체 틀 아래에 깔리도록 개체 틀을 맨 뒤(위)로 옮긴다
for l in (L_CONTENT, L_SECTION, L_TITLE):
    tree = l.shapes._spTree
    phs = [e for e in tree if e.find(".//" + qn("p:ph")) is not None]
    for e in phs:
        tree.remove(e)
        tree.append(e)

# ---------------------------------------------------------------- 슬라이드 1: 표지
s1 = prs.slides.add_slide(L_TITLE)
add_text(s1.shapes, "{EVENT}", 1.0, 1.75, 11.0, 0.5, 20, TEAL, bold=True)
add_text(s1.shapes, "{TITLE}", 1.0, 2.35, 11.3, 1.5, 44, INK, bold=True, anchor=MSO_ANCHOR.BOTTOM)
add_rect(s1.shapes, 1.0, 4.05, 1.2, 0.07, ORANGE)
add_text(s1.shapes, "{SUB}", 1.0, 4.35, 11.3, 0.9, 22, GRAY)
add_text(s1.shapes, "{AUTHOR}   ·   {DATE}", 1.0, 6.35, 11.0, 0.4, 14, GRAY)

# ---------------------------------------------------------------- 슬라이드 2: 본문 원형 (푸터 + 쪽번호)
s2 = prs.slides.add_slide(L_CONTENT)
s2.shapes.title.text = "본문 제목"
s2.placeholders[1].text = "본문"
add_text(s2.shapes, "{FOOTER}", 0.5, 7.05, 9.0, 0.3, 10, GRAY, anchor=MSO_ANCHOR.MIDDLE)
lay_num = next(p for p in L_CONTENT.placeholders if "SLIDE_NUMBER" in str(p.placeholder_format.type))
num = copy.deepcopy(lay_num._element)
txBody = num.find(qn("p:txBody"))
for p in txBody.findall(qn("a:p")):
    txBody.remove(p)
p = etree.SubElement(txBody, qn("a:p"))
etree.SubElement(p, qn("a:pPr"), algn="r")
fld = etree.SubElement(p, qn("a:fld"), id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}", type="slidenum")
r = etree.SubElement(fld, qn("a:rPr"), lang="ko-KR", sz="1000")
rgb_el(r, GRAY)
etree.SubElement(fld, qn("a:t")).text = "‹#›"
s2.shapes._spTree.append(num)

# ---------------------------------------------------------------- 슬라이드 3: 마지막
s3 = prs.slides.add_slide(L_TITLE)
add_text(s3.shapes, "Q & A", 1.0, 2.3, 11.0, 1.4, 60, INK, bold=True, anchor=MSO_ANCHOR.BOTTOM)
add_rect(s3.shapes, 1.0, 3.95, 1.2, 0.07, ORANGE)
add_text(s3.shapes, "{NEXT}", 1.0, 4.3, 11.3, 1.0, 22, GRAY)
add_text(s3.shapes, "{EVENT}", 1.0, 6.35, 11.0, 0.4, 14, TEAL, bold=True)

prs.save(OUT)
print("saved", OUT)
