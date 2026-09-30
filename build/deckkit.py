"""deckkit — AICA Lab 템플릿(Lab-template.pptx) 위에 강의 슬라이드를 쌓는 공통 빌더.

사용 예:
    from deckkit import Deck
    d = Deck(week=1, title="Tensor와 학습의 기초", subtitle="AI Zero 2 Transformer · 1주차")
    d.section("01", "Tensor란 무엇인가", "스칼라에서 4차원 텐서까지")
    d.bullets("벡터와 행렬", ["**벡터**는 숫자의 묶음", ("하위 항목", 1)], notes="...")
    d.save("lectures/week01.pptx")

인라인 마크업(모든 텍스트 공통):
    **굵게**   ==강조색==   `코드/수식(고정폭)`
좌표 단위는 inch. 본문 영역: x 0.5~12.83, y 1.05~6.95 (헤더/푸터는 템플릿이 그림).
"""
from __future__ import annotations

import copy
import math
import os
import re
from typing import Iterable

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "Lab-template.pptx")

# ---- 팔레트: 템플릿 헤더(청록 그라데이션)와 AICA 로고색에서 추출 ----
TEAL = "0F6C8C"      # 주색 (헤더 진한 청록)
TEAL2 = "3FA7B8"     # 보조색 (로고 밝은 청록)
MINT = "E6F3F6"      # 카드 배경 틴트
MINT2 = "CFE8EE"     # 강한 틴트
DARK = "1F2D3D"      # 본문 텍스트
GRAY = "5B6770"      # 캡션
LINE = "B9CBD3"      # 경계선
ACCENT = "E07A2F"    # 강조 (주황) — 핵심 수치/경고에만
ACCENT_BG = "FDF1E8"
WHITE = "FFFFFF"
CODE_BG = "F3F6F8"

FONT = "맑은 고딕"
MONO = "Courier New"

X0, X1 = 0.5, 12.83
Y0, Y1 = 1.05, 6.95
W = X1 - X0


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- text utils
_TOKEN = re.compile(r"(\*\*.+?\*\*|==.+?==|`.+?`)")


def parse_inline(text: str):
    """'**a** b `c`' -> [(text, style_dict)]"""
    out = []
    for part in _TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], {"bold": True}))
        elif part.startswith("==") and part.endswith("=="):
            out.append((part[2:-2], {"bold": True, "color": ACCENT}))
        elif part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], {"mono": True}))
        else:
            out.append((part, {}))
    return out


def _plain(text: str) -> str:
    return re.sub(r"\*\*|==|`", "", text)


def text_units(s: str) -> float:
    """대략적인 글자 폭(1.0 = 전각). 한글/한자 1.0, 라틴 0.55."""
    u = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x1100 and not (0x2000 <= o <= 0x206F):
            u += 1.0
        elif ch == " ":
            u += 0.3
        elif ch in "ilj.,:;|!'`":
            u += 0.3
        elif ch.isupper() or ch in "mwMW@%":
            u += 0.68
        else:
            u += 0.55
    return u


def est_height(paras, w_in, size, spacing=1.25, para_gap=0.35, indent_per_level=0.3):
    """문단 목록의 대략적인 높이(inch)."""
    h = 0.0
    for p in paras:
        text, lvl = (p if isinstance(p, tuple) else (p, 0))
        avail = max(0.5, w_in - 0.15 - indent_per_level * (lvl + 1 if lvl else 0.3))
        per_line = avail * 72 / size  # 전각 글자 수
        lines = max(1, math.ceil(text_units(_plain(text)) / per_line))
        h += lines * size * spacing / 72 + para_gap * size / 72
    return h + 0.12


def fit_size(paras, w_in, h_in, max_size=18, min_size=11, **kw):
    s = max_size
    while s > min_size and est_height(paras, w_in, s, **kw) > h_in:
        s -= 0.5
    return s


def _set_run_font(run, size=None, bold=None, color=None, italic=None, mono=False):
    f = run.font
    if size:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic:
        f.italic = True
    if color:
        f.color.rgb = rgb(color)
    name = MONO if mono else FONT
    f.name = name
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", FONT if tag == "a:ea" else name)


def _bullet(p, char="•", color=TEAL, lvl=0, size=16):
    pPr = p._p.get_or_add_pPr()
    indent = int(Inches(0.28 + 0.02 * (size - 14) / 4))
    pPr.set("marL", str(int(Inches(0.05 + 0.32 * lvl)) + indent))
    pPr.set("indent", str(-indent))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buClr = pPr.makeelement(qn("a:buClr"), {})
    srgb = buClr.makeelement(qn("a:srgbClr"), {"val": color})
    buClr.append(srgb)
    pPr.append(buClr)
    buFont = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
    pPr.append(buFont)
    buChar = pPr.makeelement(qn("a:buChar"), {"char": char})
    pPr.append(buChar)


def _no_bullet(p):
    pPr = p._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    pPr.set("marL", "0")
    pPr.set("indent", "0")
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def fill_tf(tf, paras, size=16, color=DARK, bold=False, align="l", bullets=False,
            spacing=1.15, para_gap=0.35, bullet_color=TEAL, anchor="t", margin=0.08):
    """paras: str | (str, level) 목록. 인라인 마크업 지원."""
    tf.word_wrap = True
    tf.auto_size = None
    m = Inches(margin)
    tf.margin_left = tf.margin_right = m
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    first = True
    for item in paras:
        text, lvl = (item if isinstance(item, tuple) else (item, 0))
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        p.line_spacing = spacing
        p.space_after = Pt(size * para_gap)
        psize = size if lvl == 0 else max(10, size - 2)
        if bullets:
            _bullet(p, char="•" if lvl == 0 else "–", color=bullet_color, lvl=lvl, size=psize)
        else:
            _no_bullet(p)
        for seg, st in parse_inline(text):
            r = p.add_run()
            r.text = seg
            _set_run_font(r, size=psize, bold=st.get("bold", bold),
                          color=st.get("color", color if lvl == 0 else (color if color != DARK else "37474F")),
                          mono=st.get("mono", False))
    return tf


# ---------------------------------------------------------------- deck
class Deck:
    def __init__(self, week: int, title: str, subtitle: str = "",
                 date: str = "2026-10-05", course: str = "AI Zero 2 Transformer",
                 author: str = "Yun-Hong Min", email: str = "picomin1027@gmail.com"):
        self.prs = Presentation(TEMPLATE)
        self.week = week
        self.date = date
        s_title, s_proto, s_last = list(self.prs.slides)
        self._proto = s_proto
        self._last = s_last
        self.layout = s_proto.slide_layout
        # 표지
        for sh in s_title.placeholders:
            idx = sh.placeholder_format.idx
            if idx == 10:
                self._set_ph(sh, course, keep_style=True)
            elif idx == 0:
                self._set_ph(sh, f"Week {week}. {title}", keep_style=True)
                if text_units(title) > 22:
                    for r in sh.text_frame.paragraphs[0].runs:
                        r.font.size = Pt(max(20, int(32 * 26 / (text_units(title) + 4))))
            elif idx == 1:
                lines = ([subtitle] if subtitle else []) + [f"{author} ({email})"]
                self._set_ph_lines(sh, lines)
                ps = sh.text_frame.paragraphs
                for k, p in enumerate(ps):
                    for r in p.runs:
                        r.font.size = Pt(18 if (subtitle and k == 0) else 15)
                        if subtitle and k == 0:
                            r.font.bold = False
        # 마지막 장
        for sh in s_last.placeholders:
            if sh.placeholder_format.idx == 10:
                self._set_ph(sh, f"E-mail: {email}", keep_style=True)
        self._footer_xml = [copy.deepcopy(sp._element) for sp in s_proto.shapes
                            if not (sp.is_placeholder and sp.placeholder_format.idx in (0, 1))]
        self.n = 0

    # -- placeholder text keeping first-run formatting
    @staticmethod
    def _set_ph(sh, text, keep_style=True):
        tf = sh.text_frame
        p0 = tf.paragraphs[0]
        runs = p0.runs
        if runs:
            runs[0].text = text
            for r in runs[1:]:
                r._r.getparent().remove(r._r)
        else:
            p0.add_run().text = text
        for p in tf.paragraphs[1:]:
            p._p.getparent().remove(p._p)

    @staticmethod
    def _set_ph_lines(sh, lines):
        tf = sh.text_frame
        base = tf.paragraphs[0]
        tmpl_p = copy.deepcopy(base._p)
        for p in list(tf.paragraphs):
            p._p.getparent().remove(p._p)
        txBody = tf._txBody
        for ln in lines:
            p = copy.deepcopy(tmpl_p)
            rs = p.findall(qn("a:r"))
            for r in rs[1:]:
                p.remove(r)
            rs[0].find(qn("a:t")).text = ln
            txBody.append(p)

    # -- new content slide with template header/footer
    def new_slide(self, title: str, notes: str | None = None):
        s = self.prs.slides.add_slide(self.layout)
        for ph in list(s.placeholders):
            idx = ph.placeholder_format.idx
            if idx == 0:
                ph.text_frame.text = ""
                r = ph.text_frame.paragraphs[0].add_run()
                r.text = title
                n = text_units(title)
                if n > 34:
                    r.font.size = Pt(max(18, int(28 * 34 / n)))
            else:
                ph._element.getparent().remove(ph._element)
        tree = s.shapes._spTree
        for el in self._footer_xml:
            el = copy.deepcopy(el)
            off = el.find(".//" + qn("a:off"))
            if off is not None and el.find(".//" + qn("p:ph")) is None:
                off.set("x", str(int(off.get("x")) - int(Inches(0.15))))
            for t in el.iter(qn("a:t")):
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.text or ""):
                    t.text = self.date
            tree.append(el)
        if notes:
            s.notes_slide.notes_text_frame.text = notes
        self.n += 1
        return s

    # ------------------------------------------------------------ primitives
    def box(self, s, x, y, w, h, fill=MINT, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
            radius=0.08, shadow=False):
        shp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(1)
        else:
            shp.line.fill.background()
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            try:
                shp.adjustments[0] = min(0.5, radius / max(0.01, min(w, h)))
            except Exception:
                pass
        if not shadow:
            spPr = shp._element.spPr
            spPr.append(spPr.makeelement(qn("a:effectLst"), {}))
        shp.text_frame.text = ""
        return shp

    def text(self, s, x, y, w, h, paras, size=16, color=DARK, bold=False, align="l",
             bullets=False, anchor="t", autofit=True, min_size=10, spacing=1.15, para_gap=0.35,
             margin=0.08, bullet_color=TEAL):
        if autofit:
            plist = [paras] if isinstance(paras, str) else paras
            size = fit_size(plist, w - 2 * margin, h, max_size=size, min_size=min_size,
                            spacing=spacing + 0.1, para_gap=para_gap)
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        fill_tf(tb.text_frame, paras, size=size, color=color, bold=bold, align=align,
                bullets=bullets, anchor=anchor, spacing=spacing, para_gap=para_gap,
                margin=margin, bullet_color=bullet_color)
        return tb

    def text_in(self, shp, paras, size=14, color=DARK, bold=False, align="l", bullets=False,
                anchor="m", min_size=9, margin=0.12, spacing=1.1, para_gap=0.25):
        w = shp.width / 914400
        h = shp.height / 914400
        plist = [paras] if isinstance(paras, str) else paras
        size = fit_size(plist, w - 2 * margin, h - 0.1, max_size=size, min_size=min_size,
                        spacing=spacing + 0.1, para_gap=para_gap)
        fill_tf(shp.text_frame, paras, size=size, color=color, bold=bold, align=align,
                bullets=bullets, anchor=anchor, margin=margin, spacing=spacing, para_gap=para_gap)
        return shp

    def arrow(self, s, x1, y1, x2, y2, color=TEAL2, width=2.0):
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color)
        c.line.width = Pt(width)
        ln = c.line._get_or_add_ln()
        ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
        return c

    def circle_num(self, s, x, y, d, label, fill=TEAL, color=WHITE, size=14):
        c = self.box(s, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL)
        self.text_in(c, str(label), size=size, color=color, bold=True, align="c", margin=0.0)
        return c

    def lead(self, s, text, y=Y0, h=0.55, size=17):
        """제목 아래 한 줄 요지(굵은 청록)."""
        return self.text(s, X0, y, W, h, text, size=size, color=TEAL, bold=True, anchor="m", min_size=12)

    # ------------------------------------------------------------ slide types
    def section(self, num: str, title: str, subtitle: str = "", notes: str | None = None,
                header: str | None = None):
        """구역 표지: 큰 번호 + 제목."""
        s = self.new_slide(header or f"Week {self.week} · Part {num}", notes)
        self.box(s, 0.9, 2.0, 11.5, 3.3, fill=MINT)
        self.text(s, 1.3, 2.25, 2.4, 2.8, num, size=80, color=TEAL, bold=True, anchor="m",
                  autofit=False)
        self.text(s, 3.8, 2.35, 8.3, 1.4, title, size=36, color=DARK, bold=True, anchor="b", min_size=24)
        if subtitle:
            self.text(s, 3.8, 3.85, 8.3, 1.2, subtitle, size=18, color=GRAY, anchor="t", min_size=12)
        return s

    def bullets(self, title: str, items, notes: str | None = None, lead: str | None = None,
                side: dict | None = None, size=18):
        """글머리표. side={'head':..,'body':[..]} 또는 {'image': path, 'caption':..} 이면 오른쪽 패널."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        w = W if not side else 6.9
        self.text(s, X0, y + 0.1, w, Y1 - y - 0.1, items, size=size, bullets=True, min_size=11,
                  para_gap=0.55)
        if side:
            self._side_panel(s, X0 + 7.2, y + 0.1, W - 7.2, Y1 - y - 0.15, side)
        return s

    def _side_panel(self, s, x, y, w, h, side):
        if "image" in side:
            cap_h = 0.45 if side.get("caption") else 0
            self._image_fit(s, side["image"], x, y, w, h - cap_h)
            if cap_h:
                self.text(s, x, y + h - cap_h, w, cap_h, side["caption"], size=12, color=GRAY,
                          align="c", anchor="m")
            return
        fill = ACCENT_BG if side.get("accent") else MINT
        hc = ACCENT if side.get("accent") else TEAL
        self.box(s, x, y, w, h, fill=fill)
        yy = y + 0.2
        if side.get("head"):
            self.text(s, x + 0.2, yy, w - 0.4, 0.55, side["head"], size=18, bold=True, color=hc, anchor="m")
            yy += 0.65
        body = side.get("body", [])
        self.text(s, x + 0.2, yy, w - 0.4, y + h - yy - 0.15, body, size=15,
                  bullets=side.get("bullets", True), min_size=10, para_gap=0.45)

    def _image_fit(self, s, path, x, y, w, h):
        from PIL import Image
        with Image.open(path) as im:
            iw, ih = im.size
        r = min(w / iw, h / ih)
        pw, ph = iw * r, ih * r
        return s.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2),
                                    Inches(pw), Inches(ph))

    def cards(self, title: str, cards: list[dict], cols: int | None = None, notes=None,
              lead: str | None = None, numbered=False, footer: str | None = None):
        """cards: [{'head':..., 'body': str|[..], 'tag': 'optional small label', 'accent':bool}]"""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        bottom = Y1 - (0.75 if footer else 0)
        n = len(cards)
        cols = cols or (n if n <= 4 else (3 if n in (5, 6, 9) else 4))
        rows = math.ceil(n / cols)
        gap = 0.3
        cw = (W - gap * (cols - 1)) / cols
        ch = (bottom - y - 0.1 - gap * (rows - 1)) / rows
        for i, c in enumerate(cards):
            r, k = divmod(i, cols)
            cx = X0 + k * (cw + gap)
            cy = y + 0.1 + r * (ch + gap)
            acc = c.get("accent")
            self.box(s, cx, cy, cw, ch, fill=ACCENT_BG if acc else MINT)
            hx = cx + 0.2
            if numbered:
                self.circle_num(s, cx + 0.2, cy + 0.2, 0.5, i + 1, fill=ACCENT if acc else TEAL)
                hx = cx + 0.85
            yy = cy + 0.15
            if c.get("tag"):
                self.text(s, hx, yy, cx + cw - hx - 0.15, 0.35, c["tag"], size=12,
                          color=ACCENT if acc else TEAL2, bold=True, anchor="m")
                yy += 0.35
            self.text(s, hx, yy, cx + cw - hx - 0.15, 0.62, c["head"], size=19, bold=True,
                      color=ACCENT if acc else TEAL, anchor="m", min_size=13)
            yy = max(yy + 0.7, cy + 0.85 if numbered else 0)
            body = c.get("body", [])
            self.text(s, cx + 0.2, yy, cw - 0.35, cy + ch - yy - 0.12, body, size=15,
                      bullets=isinstance(body, list) and len(body) > 1, min_size=10, para_gap=0.4)
        if footer:
            self.takeaway(s, footer)
        return s

    def takeaway(self, s, text, y=Y1 - 0.62, h=0.6):
        b = self.box(s, X0, y, W, h, fill=TEAL)
        self.text_in(b, text, size=16, color=WHITE, bold=True, align="c", margin=0.2)
        return b

    def timeline(self, title: str, events: list[tuple], notes=None, lead: str | None = None,
                 highlight: Iterable[int] = ()):
        """events: [(year, head, body)] — 가로 타임라인(최대 7개 권장)."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        n = len(events)
        line_y = y + 1.05
        self.box(s, X0, line_y - 0.03, W, 0.06, fill=LINE, shape=MSO_SHAPE.RECTANGLE)
        gap = 0.18
        cw = (W - gap * (n - 1)) / n
        hl = set(highlight)
        for i, (yr, head, body) in enumerate(events):
            cx = X0 + i * (cw + gap)
            acc = i in hl
            col = ACCENT if acc else TEAL
            self.text(s, cx, y, cw, 0.6, str(yr), size=22, bold=True, color=col, align="c",
                      anchor="b", min_size=12)
            d = 0.26
            self.box(s, cx + cw / 2 - d / 2, line_y - d / 2, d, d, fill=col, shape=MSO_SHAPE.OVAL)
            by = line_y + 0.35
            self.box(s, cx, by, cw, Y1 - by, fill=ACCENT_BG if acc else MINT)
            self.text(s, cx + 0.1, by + 0.1, cw - 0.2, 0.9, head, size=16, bold=True, color=col,
                      align="c", anchor="m", min_size=11)
            self.text(s, cx + 0.1, by + 1.05, cw - 0.2, Y1 - by - 1.15, body, size=13,
                      color=DARK, min_size=9, para_gap=0.3)
        return s

    def flow(self, title: str, steps: list[dict | str], notes=None, lead: str | None = None,
             caption: str | None = None, below: list | None = None):
        """가로 흐름도: steps=[{'head':..,'body':..}] 사이에 화살표. below: 아래 글머리표."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.75
        n = len(steps)
        ag = 0.45
        bw = (W - ag * (n - 1)) / n
        bh = 2.0 if below else (Y1 - y - (0.7 if caption else 0.2))
        bh = min(bh, 3.2)
        for i, st in enumerate(steps):
            st = st if isinstance(st, dict) else {"head": st}
            bx = X0 + i * (bw + ag)
            acc = st.get("accent")
            b = self.box(s, bx, y + 0.1, bw, bh, fill=ACCENT_BG if acc else MINT,
                         line=ACCENT if acc else None)
            self.text(s, bx + 0.1, y + 0.2, bw - 0.2, 0.7, st["head"], size=17, bold=True,
                      color=ACCENT if acc else TEAL, align="c", anchor="m", min_size=11)
            if st.get("body"):
                self.text(s, bx + 0.1, y + 0.9, bw - 0.2, bh - 0.9, st["body"], size=13,
                          align="c", min_size=9, para_gap=0.25)
            if i < n - 1:
                ax = bx + bw + 0.05
                self.arrow(s, ax, y + 0.1 + bh / 2, ax + ag - 0.1, y + 0.1 + bh / 2)
        yy = y + 0.1 + bh + 0.3
        if below:
            self.text(s, X0, yy, W, Y1 - yy - (0.7 if caption else 0), below, size=16, bullets=True,
                      min_size=11, para_gap=0.45)
        if caption:
            self.takeaway(s, caption)
        return s

    def formula(self, title: str, formula: str | list, parts: list[tuple] | None = None,
                notes=None, lead: str | None = None, takeaway: str | None = None,
                example: list | str | None = None):
        """핵심 수식 강조. formula: 고정폭 수식 한두 줄. parts: [(기호, 의미)]. example: 오른쪽/아래 수치 예."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        lines = formula if isinstance(formula, list) else [formula]
        fh = 0.35 + 0.62 * len(lines)
        b = self.box(s, X0, y + 0.1, W, fh, fill=CODE_BG, line=LINE)
        tb = s.shapes.add_textbox(Inches(X0 + 0.2), Inches(y + 0.15), Inches(W - 0.4), Inches(fh - 0.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        longest = max(len(l) for l in lines)
        fsize = 26 if longest <= 48 else max(14, int(26 * 48 / longest))
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            _no_bullet(p)
            r = p.add_run()
            r.text = ln
            _set_run_font(r, size=fsize, bold=True, color=DARK, mono=True)
        yy = y + 0.1 + fh + 0.3
        bottom = Y1 - (0.72 if takeaway else 0)
        if parts and example:
            lw = 6.9
        else:
            lw = W
        if parts:
            rows = len(parts)
            rh = min(0.62, (bottom - yy) / max(rows, 1))
            for i, (sym, mean) in enumerate(parts):
                ry = yy + i * rh
                self.box(s, X0, ry + 0.04, 1.9, rh - 0.08, fill=MINT2)
                self.text(s, X0, ry + 0.04, 1.9, rh - 0.08, f"`{sym}`" if "`" not in sym else sym,
                          size=15, bold=True, align="c", anchor="m", min_size=10)
                self.text(s, X0 + 2.0, ry, lw - 2.0, rh, mean, size=15, anchor="m", min_size=10)
        if example:
            ex_x = X0 + (lw + 0.3 if parts else 0)
            ex_w = W - (lw + 0.3 if parts else 0)
            self.box(s, ex_x, yy, ex_w, bottom - yy - 0.1, fill=ACCENT_BG)
            self.text(s, ex_x + 0.2, yy + 0.1, ex_w - 0.4, 0.45, "숫자로 확인", size=15, bold=True,
                      color=ACCENT, anchor="m")
            self.text(s, ex_x + 0.2, yy + 0.6, ex_w - 0.4, bottom - yy - 0.8, example, size=14,
                      min_size=9, para_gap=0.3)
        if takeaway:
            self.takeaway(s, takeaway)
        return s

    def table(self, title: str, header: list[str], rows: list[list[str]], notes=None,
              lead: str | None = None, col_widths: list[float] | None = None, takeaway=None,
              size=14, highlight_rows: Iterable[int] = ()):
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        bottom = Y1 - (0.75 if takeaway else 0)
        nr, nc = len(rows) + 1, len(header)
        col_widths = col_widths or [W / nc] * nc
        tot = sum(col_widths)
        col_widths = [c * W / tot for c in col_widths]
        # 높이 추정
        def row_h(cells, sz):
            return max(est_height([c], cw, sz, spacing=1.2, para_gap=0) for c, cw in zip(cells, col_widths)) + 0.08
        sz = size
        while sz > 9 and sum(row_h(r, sz) for r in [header] + rows) > bottom - y - 0.1:
            sz -= 0.5
        heights = [row_h(r, sz) for r in [header] + rows]
        gt = s.shapes.add_table(nr, nc, Inches(X0), Inches(y + 0.1), Inches(W), Inches(sum(heights)))
        tbl = gt.table
        tblPr = tbl._tbl.tblPr
        for k in ("bandRow", "firstRow"):
            tblPr.set(k, "0")
        # 스타일 제거
        sid = tblPr.find(qn("a:tableStyleId"))
        if sid is not None:
            sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # No Style, Table Grid
        for j, cw in enumerate(col_widths):
            tbl.columns[j].width = Inches(cw)
        hl = set(highlight_rows)
        for i, r in enumerate([header] + rows):
            tbl.rows[i].height = Inches(heights[i])
            for j, val in enumerate(r):
                cell = tbl.cell(i, j)
                cell.margin_left = cell.margin_right = Inches(0.08)
                cell.margin_top = cell.margin_bottom = Inches(0.04)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.fill.solid()
                if i == 0:
                    cell.fill.fore_color.rgb = rgb(TEAL)
                elif (i - 1) in hl:
                    cell.fill.fore_color.rgb = rgb(ACCENT_BG)
                else:
                    cell.fill.fore_color.rgb = rgb(WHITE if i % 2 else MINT)
                tf = cell.text_frame
                fill_tf(tf, [str(val)], size=sz, color=WHITE if i == 0 else DARK, bold=(i == 0 or j == 0),
                        align="c" if i == 0 else "l", margin=0.06, para_gap=0)
                self._cell_border(cell)
        if takeaway:
            self.takeaway(s, takeaway)
        return s

    @staticmethod
    def _cell_border(cell, color=LINE):
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
            ln = tcPr.makeelement(qn(tag), {"w": "6350"})
            sf = ln.makeelement(qn("a:solidFill"), {})
            sf.append(sf.makeelement(qn("a:srgbClr"), {"val": color}))
            ln.append(sf)
            tcPr.insert(0, ln) if False else tcPr.append(ln)
        # schema order: lnL lnR lnT lnB ... solidFill must follow; move fill to the end
        for f in tcPr.findall(qn("a:solidFill")):
            tcPr.remove(f)
            tcPr.append(f)

    def compare(self, title: str, left: dict, right: dict, notes=None, lead=None, takeaway=None,
                vs: str = "→"):
        """좌우 비교. left/right = {'head':..,'body':[..], 'accent':bool}"""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        bottom = Y1 - (0.75 if takeaway else 0)
        gap = 0.8
        cw = (W - gap) / 2
        for k, side in enumerate((left, right)):
            cx = X0 + k * (cw + gap)
            acc = side.get("accent")
            self.box(s, cx, y + 0.1, cw, bottom - y - 0.2, fill=ACCENT_BG if acc else MINT)
            self.text(s, cx + 0.25, y + 0.2, cw - 0.5, 0.65, side["head"], size=21, bold=True,
                      color=ACCENT if acc else TEAL, anchor="m", min_size=13)
            self.text(s, cx + 0.25, y + 0.95, cw - 0.5, bottom - y - 1.2, side.get("body", []),
                      size=16, bullets=True, min_size=10, para_gap=0.45)
        c = self.circle_num(s, X0 + cw + gap / 2 - 0.3, (y + bottom) / 2 - 0.3, 0.6, vs,
                            fill=TEAL2, size=18)
        if takeaway:
            self.takeaway(s, takeaway)
        return s

    def code(self, title: str, code: str, notes=None, lead=None, explain: list | None = None,
             code_size=14):
        """코드 블록(왼쪽) + 설명(오른쪽)."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        cw = W if not explain else 7.4
        self.box(s, X0, y + 0.1, cw, Y1 - y - 0.1, fill=CODE_BG, line=LINE, radius=0.05)
        lines = code.rstrip("\n").split("\n")
        avail_h = Y1 - y - 0.4
        longest = max(len(l) for l in lines)
        sz = code_size
        while sz > 9 and (len(lines) * sz * 1.2 / 72 > avail_h or longest * sz * 0.6 / 72 > cw - 0.4):
            sz -= 0.5
        tb = s.shapes.add_textbox(Inches(X0 + 0.15), Inches(y + 0.2), Inches(cw - 0.3), Inches(Y1 - y - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            _no_bullet(p)
            p.line_spacing = 1.0
            r = p.add_run()
            r.text = ln if ln else " "
            is_comment = ln.strip().startswith("#")
            _set_run_font(r, size=sz, color="5E8C6A" if is_comment else DARK, mono=True)
        if explain:
            ex = X0 + cw + 0.3
            self.text(s, ex, y + 0.1, X1 - ex, Y1 - y - 0.1, explain, size=16, bullets=True,
                      min_size=10, para_gap=0.5)
        return s

    def image(self, title: str, path: str, notes=None, lead=None, caption=None,
              side: list | dict | None = None, img_w_ratio=0.58):
        """그림(matplotlib 등) + 선택적 오른쪽 설명."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        cap_h = 0.45 if caption else 0
        iw = W * img_w_ratio if side else W
        self._image_fit(s, path, X0, y + 0.1, iw, Y1 - y - 0.15 - cap_h)
        if caption:
            self.text(s, X0, Y1 - cap_h, iw, cap_h, caption, size=12, color=GRAY, align="c", anchor="m")
        if side:
            sx = X0 + iw + 0.3
            if isinstance(side, dict):
                self._side_panel(s, sx, y + 0.1, X1 - sx, Y1 - y - 0.15, side)
            else:
                self.text(s, sx, y + 0.1, X1 - sx, Y1 - y - 0.15, side, size=16, bullets=True,
                          min_size=10, para_gap=0.5)
        return s

    def stats(self, title: str, stats: list[tuple], notes=None, lead=None, below: list | None = None):
        """큰 숫자 강조: stats=[(big, label)]."""
        s = self.new_slide(title, notes)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        n = len(stats)
        gap = 0.3
        cw = (W - gap * (n - 1)) / n
        bh = 2.2
        for i, (big, label) in enumerate(stats):
            cx = X0 + i * (cw + gap)
            self.box(s, cx, y + 0.1, cw, bh, fill=MINT)
            self.text(s, cx + 0.1, y + 0.2, cw - 0.2, 1.2, big, size=48, bold=True, color=ACCENT,
                      align="c", anchor="m", min_size=20)
            self.text(s, cx + 0.15, y + 1.4, cw - 0.3, bh - 1.35, label, size=15, align="c",
                      min_size=10, anchor="t")
        if below:
            yy = y + 0.1 + bh + 0.35
            self.text(s, X0, yy, W, Y1 - yy, below, size=16, bullets=True, min_size=11, para_gap=0.5)
        return s

    def quiz(self, title: str, questions: list[tuple], notes=None, lead=None):
        """확인 문제: [(질문, 정답/해설)] — 질문은 슬라이드, 정답은 노트에 자동 기록."""
        ans = "\n".join(f"Q{i+1}. {_plain(q)}\n  → {_plain(a)}" for i, (q, a) in enumerate(questions))
        s = self.new_slide(title, (notes + "\n\n" if notes else "") + "[정답]\n" + ans)
        y = Y0
        if lead:
            self.lead(s, lead)
            y += 0.7
        n = len(questions)
        gap = 0.2
        rh = (Y1 - y - 0.1 - gap * (n - 1)) / n
        for i, (q, _) in enumerate(questions):
            ry = y + 0.1 + i * (rh + gap)
            self.box(s, X0, ry, W, rh, fill=MINT)
            d = min(0.55, rh - 0.15)
            self.circle_num(s, X0 + 0.2, ry + (rh - d) / 2, d, f"Q{i+1}", size=13)
            self.text(s, X0 + 0.95, ry, W - 1.1, rh, q, size=17, anchor="m", min_size=10)
        return s

    def summary(self, title: str, items: list[str], notes=None, next_week: str | None = None):
        """번호 원 + 요약 문장. next_week 이 있으면 하단에 '다음 주' 박스."""
        s = self.new_slide(title, notes)
        bottom = Y1 - (0.8 if next_week else 0)
        n = len(items)
        gap = 0.15
        rh = min(0.95, (bottom - Y0 - 0.1 - gap * (n - 1)) / n)
        for i, it in enumerate(items):
            ry = Y0 + 0.1 + i * (rh + gap)
            d = min(0.55, rh - 0.1)
            self.circle_num(s, X0, ry + (rh - d) / 2, d, i + 1, size=15)
            self.text(s, X0 + d + 0.25, ry, W - d - 0.3, rh, it, size=18, anchor="m", min_size=11)
        if next_week:
            b = self.box(s, X0, Y1 - 0.65, W, 0.65, fill=ACCENT_BG)
            self.text_in(b, f"**다음 주 →** {next_week}", size=16, color=DARK, align="l", margin=0.25)
        return s

    def blank(self, title: str, notes=None):
        """자유 배치용 빈 본문 슬라이드(헤더/푸터 포함)."""
        return self.new_slide(title, notes)

    # ------------------------------------------------------------ save
    def save(self, path: str):
        prs = self.prs
        sldIdLst = prs.slides._sldIdLst
        ids = list(sldIdLst)
        # 원본 예시(2번) 삭제, 마지막 장을 맨 뒤로
        proto_id, last_id = ids[1], ids[2]
        prs.part.drop_rel(proto_id.rId)
        sldIdLst.remove(proto_id)
        sldIdLst.remove(last_id)
        sldIdLst.append(last_id)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        prs.save(path)
        return path


# ------------------------------------------------------------ matplotlib helper
def mpl_setup():
    """한글 폰트가 설정된 matplotlib.pyplot 반환."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("/usr/share/fonts/truetype/nanum/NanumGothic.ttf",):
        if os.path.exists(f):
            font_manager.fontManager.addfont(f)
            plt.rcParams["font.family"] = "NanumGothic"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["axes.edgecolor"] = "#" + LINE
    plt.rcParams["axes.labelcolor"] = "#" + DARK
    plt.rcParams["xtick.color"] = "#" + GRAY
    plt.rcParams["ytick.color"] = "#" + GRAY
    plt.rcParams["savefig.dpi"] = 200
    plt.rcParams["savefig.bbox"] = "tight"
    return plt


PALETTE_HEX = {k: "#" + v for k, v in dict(TEAL=TEAL, TEAL2=TEAL2, MINT=MINT, DARK=DARK, GRAY=GRAY,
                                           ACCENT=ACCENT, LINE=LINE).items()}
