"""Week 6 논문 그림 (독립 실행): python build/paper_figs_w6.py -> build/assets/week6/*.png

원문 표·그림의 수치를 matplotlib으로 새로 그린다(원본 이미지 사용 안 함).
수치 출처는 build/research/papers/week6.md (각 함수 docstring에 원문 위치).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")
from deckkit import mpl_setup, PALETTE_HEX as P  # noqa: E402

import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager as _fm  # noqa: E402
for _f in ("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",):
    if os.path.exists(_f):
        _fm.fontManager.addfont(_f)
_fm.fontManager._findfont_cached.cache_clear()

OUT = os.path.join(HERE, "assets", "week6")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "DARK", "GRAY", "ACCENT", "LINE"))
MINT, MINT2 = P["MINT"], P.get("MINT2", "#D6E6FA")
ACC_MID, ACC_BG = P.get("ACC_MID", "#FBD3B8"), P.get("ACC_BG", "#FFF3EA")
BG, GRID, MID, OFF = P.get("BG", "#F5F5F7"), P.get("GRID", "#ECECF0"), P.get("MID", "#9CC5F2"), P.get("OFF", "#E8E8ED")
plt.rcParams.update({"font.size": 14, "axes.labelsize": 15, "xtick.labelsize": 13.5, "ytick.labelsize": 13.5,
                     "axes.titlesize": 15})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def clean(ax, grid="y"):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.9)
        ax.set_axisbelow(True)


def src(fig, text, y=-0.02):
    fig.text(0.99, y, text, ha="right", va="top", fontsize=11.5, color=GRAY)


# ------------------------------------------------------------------ Table 2: 결과와 비용
def fig_table2():
    """Vaswani 2017 Table 2 (newstest2014 EN-DE BLEU, 학습 비용 FLOPs)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})
    names = ["MoE", "GNMT+RL\nEnsemble", "ConvS2S\nEnsemble", "Transformer\nbase", "Transformer\nbig"]
    bleu = [26.03, 26.30, 26.36, 27.3, 28.4]
    cols = [OFF, OFF, OFF, TEAL2, TEAL]
    b = a1.bar(range(5), bleu, color=cols, width=0.62)
    for i, v in enumerate(bleu):
        a1.text(i, v + 0.06, f"{v:g}", ha="center", va="bottom", fontsize=14, fontweight="bold",
                color=TEAL if i >= 3 else GRAY)
    a1.set_xticks(range(5))
    a1.set_xticklabels(names, fontsize=12.5)
    a1.set_ylim(25.0, 29.0)
    a1.set_ylabel("EN→DE BLEU")
    a1.set_title("번역 품질 (높을수록 좋음)", loc="left", color=DARK, fontweight="bold")
    clean(a1)
    names2 = ["Transformer\nbase", "Transformer\nbig", "ConvS2S\nEnsemble"]
    cost = [3.3e18, 2.3e19, 7.7e19]
    a2.bar(range(3), cost, color=[TEAL2, TEAL, OFF], width=0.58)
    a2.set_yscale("log")
    a2.set_ylim(1e18, 3e20)
    for i, v in enumerate(cost):
        m, e = f"{v:.1e}".split("e")
        a2.text(i, v * 1.25, f"{float(m):g}·10$^{{{int(e)}}}$", ha="center", va="bottom", fontsize=14,
                fontweight="bold", color=TEAL if i < 2 else GRAY)
    a2.set_xticks(range(3))
    a2.set_xticklabels(names2, fontsize=12.5)
    a2.set_ylabel("학습 FLOPs (로그 축)")
    a2.set_title("학습 비용 (낮을수록 좋음)", loc="left", color=DARK, fontweight="bold")
    clean(a2)
    fig.tight_layout(w_pad=3)
    src(fig, "원문 Table 2 기반 재구성 (EN→DE, newstest2014)")
    save(fig, "p_table2.png")


# ------------------------------------------------------------------ Table 3: 변형 실험
def fig_table3():
    """Vaswani 2017 Table 3 (EN-DE dev newstest2013, 단일 실행, 체크포인트 평균 없음)."""
    fig, axs = plt.subplots(1, 3, figsize=(14.5, 4.7))
    # (A) head 수 (계산량 고정)
    a = axs[0]
    h = ["1", "4", "8\n(base)", "16", "32"]
    bl = [24.9, 25.5, 25.8, 25.8, 25.4]
    a.bar(range(5), bl, color=[OFF, MID, TEAL, MID, OFF], width=0.6)
    for i, v in enumerate(bl):
        a.text(i, v + 0.05, f"{v:g}", ha="center", va="bottom", fontsize=13.5, fontweight="bold",
               color=TEAL if i == 2 else DARK)
    a.set_xticks(range(5))
    a.set_xticklabels(h)
    a.set_ylim(24.0, 26.4)
    a.set_xlabel("head 수 h  (h·d_k = 512 고정)")
    a.set_ylabel("dev BLEU")
    a.set_title("(A) head는 많을수록 좋은가?", loc="left", fontweight="bold", color=DARK)
    clean(a)
    # (C) 크기
    a = axs[1]
    pts = [("N=2", 36, 23.7), ("N=4", 50, 25.3), ("N=8", 80, 25.5), ("d=256", 28, 24.5), ("d=1024", 168, 26.0),
           ("d_ff=1024", 53, 25.4), ("d_ff=4096", 90, 26.2)]
    for lab, p, v in pts:
        a.plot(p, v, "o", ms=10, color=TEAL2, mec="white", mew=1.5)
        dx, dy, ha = 1.08, 0.0, "left"
        if lab in ("d=1024",):
            dx, ha = 0.93, "right"
        if lab == "N=4":
            dx, dy, ha = 0.93, -0.05, "right"
        if lab == "d_ff=1024":
            dx, dy = 1.0, 0.17
        if lab == "N=8":
            dy = -0.14
        a.text(p * dx, v + dy, lab, fontsize=12, color=DARK, ha=ha, va="center")
    a.plot(65, 25.8, "o", ms=12, color=TEAL, mec="white", mew=1.5)
    a.text(65 * 0.92, 25.95, "base 65M", fontsize=12.5, color=TEAL, ha="right", fontweight="bold")
    a.set_xscale("log")
    from matplotlib.ticker import NullFormatter, NullLocator
    a.xaxis.set_minor_locator(NullLocator())
    a.xaxis.set_minor_formatter(NullFormatter())
    a.set_xticks([30, 60, 120, 240])
    a.set_xticklabels(["30M", "60M", "120M", "240M"])
    a.set_xlim(22, 260)
    a.set_ylim(23.4, 26.6)
    a.set_xlabel("파라미터 수 (로그 축)")
    a.set_title("(C) 크게 만들면?", loc="left", fontweight="bold", color=DARK)
    clean(a, grid="both")
    # (D) label smoothing: PPL과 BLEU가 반대로
    a = axs[2]
    eps = [0.0, 0.1, 0.2]
    ppl = [4.67, 4.92, 5.47]
    bl = [25.3, 25.8, 25.7]
    a.plot(eps, ppl, "o-", color=ACC, lw=2.4, ms=10, mec="white", mew=1.5)
    a.set_ylabel("dev PPL (낮을수록 좋음)", color=ACC)
    a.set_ylim(4.4, 5.75)
    a.tick_params(axis="y", colors=ACC)
    for e, v, (dx, dy) in zip(eps, ppl, [(0, -0.15), (0.0, -0.15), (-0.03, 0.04)]):
        a.text(e + dx, v + dy, f"{v:g}", ha="center", color=ACC, fontsize=13, fontweight="bold")
    b2 = a.twinx()
    b2.plot(eps, bl, "s--", color=TEAL, lw=2.4, ms=9, mec="white", mew=1.5)
    b2.set_ylim(24.9, 26.1)
    b2.set_ylabel("dev BLEU (높을수록 좋음)", color=TEAL)
    b2.tick_params(axis="y", colors=TEAL)
    for e, v in zip(eps, bl):
        b2.text(e, v + 0.05, f"{v:g}", ha="center", color=TEAL, fontsize=13, fontweight="bold")
    for sp in ("top",):
        a.spines[sp].set_visible(False)
        b2.spines[sp].set_visible(False)
    a.set_xticks(eps)
    a.set_xlim(-0.04, 0.24)
    a.set_xlabel("label smoothing ε_ls")
    a.set_title("(D) ε_ls: PPL ↔ BLEU 반대", loc="left", fontweight="bold", color=DARK)
    fig.tight_layout(w_pad=2.2)
    src(fig, "원문 Table 3 (A)(C)(D) 기반 재구성 — dev set, 단일 실행, 체크포인트 평균 없음")
    save(fig, "p_table3.png")


# ------------------------------------------------------------------ 파라미터: 공식 vs 논문
def fig_param_gap():
    """우리 공식(4d²+2d·d_ff per enc layer, 8d²+2d·d_ff per dec layer, 37k×d 공유 임베딩) vs Table 3 params."""
    rows = [("base", 512, 62.98, 65), ("N=2", 512, 33.7, 36), ("N=4", 512, 48.4, 50), ("N=8", 512, 77.8, 80),
            ("d_k=16", 512, 56.0, 58), ("d_k=32", 512, 58.4, 60), ("d_ff=1024", 512, 50.5, 53),
            ("d_ff=4096", 512, 88.3, 90), ("d=256", 256, 26.8, 28), ("d=1024", 1024, 163.9, 168),
            ("big", 1024, 214.2, 213)]
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    cmap = {256: GRAY, 512: TEAL2, 1024: ACC}
    for i, (lab, d, f, p) in enumerate(rows):
        g = p - f
        ax.barh(i, g, color=cmap[d], height=0.62)
        ax.text(g + (0.08 if g >= 0 else -0.08), i, f"{g:+.1f}M", va="center", ha="left" if g >= 0 else "right",
                fontsize=12.5, color=DARK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{r[0]}  ({r[3]}M)" for r in rows], fontsize=12.5)
    ax.invert_yaxis()
    ax.axvline(0, color=GRAY, lw=1)
    ax.set_xlim(-2.2, 6.2)
    ax.set_xlabel("논문 값 - 우리 공식 (M)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=f"d = {d}") for d, c in cmap.items()], frameon=False,
              loc="upper right", fontsize=12.5)
    clean(ax, grid="x")
    src(fig, "원문 Table 3 params 열 + 우리 계산 (bias·LN 제외, 어휘 37,000)")
    save(fig, "p_param_gap.png")


# ------------------------------------------------------------------ Xiong Theorem 1: 상한 비
def fig_xiong():
    """Xiong 2020 Theorem 1: Post-LN O(d√ln d), Pre-LN O(d√(ln d / L)) → 비 1/√L (상수 무시)."""
    L = np.arange(1, 25)
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(L, np.ones_like(L, dtype=float), color=ACC, lw=2.6)
    ax.text(24.3, 1.0, "Post-LN\n(L과 무관)", color=ACC, fontsize=13.5, va="center", fontweight="bold")
    ax.plot(L, 1 / np.sqrt(L), color=TEAL, lw=2.6)
    ax.text(17, 0.1, "Pre-LN  ∝ 1/√L", color=TEAL, fontsize=13.5, va="center", ha="center", fontweight="bold")
    for l in (6, 12, 24):
        v = 1 / np.sqrt(l)
        ax.plot(l, v, "o", ms=10, color=TEAL, mec="white", mew=2)
        ax.text(l, v + 0.07, f"{v:.2f}", ha="center", fontsize=13.5, color=TEAL, fontweight="bold")
    ax.set_xlim(0, 29.5)
    ax.set_ylim(0, 1.25)
    ax.set_xticks([1, 6, 12, 18, 24])
    ax.set_xlabel("층 수 L")
    ax.set_ylabel("마지막 FFN 기울기 상한\n(Post-LN = 1로 둔 비)")
    clean(ax)
    src(fig, "Xiong et al. (2020) Theorem 1의 상한끼리의 비 — 우리 계산, 실측값 아님")
    save(fig, "p_xiong_bound.png")


# ------------------------------------------------------------------ MHA / GQA / MQA
def fig_gqa():
    """Ainslie 2023 Figure 2 (도식) 재구성 + Table 1 (T5 XXL, 5% uptraining)."""
    fig = plt.figure(figsize=(11.8, 4.4))
    ax = fig.add_axes([0.0, 0.02, 0.56, 0.94])
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 6)
    ax.axis("off")
    groups = [("MHA", 8), ("GQA-2", 2), ("MQA", 1)]
    for gi, (name, g) in enumerate(groups):
        x0 = 0.3 + gi * 5.0
        ax.text(x0 + 2.0, 5.55, name, ha="center", fontsize=16, fontweight="bold", color=[TEAL, TEAL2, ACC][gi])
        qx = [x0 + i * 0.52 for i in range(8)]
        for i, x in enumerate(qx):
            ax.add_patch(FancyBboxPatch((x, 3.9), 0.38, 0.9, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        fc=MINT2, ec="none"))
        ax.text(x0 - 0.05, 4.35, "Q", ha="right", va="center", fontsize=13.5, color=DARK)
        span = 8 / g
        for k in range(g):
            cx = x0 + (k * span + span / 2) * 0.52 - 0.33
            w = 0.38 if g == 8 else 0.62
            cx = qx[k] if g == 8 else cx
            ax.add_patch(FancyBboxPatch((cx, 1.15), w, 0.9, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        fc=ACC_MID if g < 8 else OFF, ec="none"))
            for i in range(int(k * span), int((k + 1) * span)):
                ax.plot([qx[i] + 0.19, cx + w / 2], [3.88, 2.08], color=GRAY, lw=1.0)
        ax.text(x0 - 0.05, 1.6, "K,V", ha="right", va="center", fontsize=13.5, color=DARK)
        ax.text(x0 + 2.0, 0.45, f"K/V head {g}벌", ha="center", fontsize=14, color=DARK)
    ax.text(7.5, -0.15, "원문 Figure 2 기반 재구성 (Query head 8개 예)", ha="center", fontsize=11.5, color=GRAY)
    a = fig.add_axes([0.64, 0.17, 0.34, 0.72])
    pts = [("MHA-XXL", 1.51, 47.2, TEAL), ("MQA-XXL", 0.24, 46.6, ACC), ("GQA-8-XXL", 0.28, 47.1, TEAL2),
           ("MHA-Large", 0.37, 46.0, GRAY)]
    for lab, t, s, c in pts:
        a.plot(t, s, "o", ms=12, color=c, mec="white", mew=1.5)
        dx, ha = (0.07, "left")
        dy = 0.0
        if lab == "MQA-XXL":
            dy = -0.13
        if lab == "GQA-8-XXL":
            dy = 0.12
        if lab == "MHA-XXL":
            dx, ha = (-0.07, "right")
        a.text(t + dx, s + dy, lab, ha=ha, va="center", fontsize=12.5, color=c, fontweight="bold")
    a.set_xlim(0, 1.75)
    a.set_ylim(45.7, 47.5)
    a.set_xlabel("추론 시간 / 샘플 (s)")
    a.set_ylabel("평균 점수")
    clean(a, grid="both")
    a.set_title("원문 Table 1 (T5, 5% uptraining)", fontsize=12.5, color=GRAY, loc="left")
    save(fig, "p_gqa.png")


# ------------------------------------------------------------------ FlashAttention Figure 2
def fig_flash():
    """Dao 2022 Figure 2 좌측 표 (GPT-2 medium, N=1024, d=64, 16 head, batch 64, A100, fwd+bwd)."""
    fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.9))
    data = [("연산량 GFLOPs", 66.6, 75.2), ("HBM 읽기·쓰기 (GB)", 40.3, 4.4), ("실행 시간 (ms)", 41.7, 7.3)]
    for a, (t, s, f) in zip(axs, data):
        a.bar([0, 1], [s, f], color=[OFF, TEAL], width=0.6)
        top = max(s, f)
        for i, v in enumerate([s, f]):
            a.text(i, v + top * 0.03, f"{v:g}", ha="center", va="bottom", fontsize=15, fontweight="bold",
                   color=TEAL if i else GRAY)
        a.set_xticks([0, 1])
        a.set_xticklabels(["표준", "Flash"], fontsize=14)
        a.set_ylim(0, top * 1.22)
        a.set_title(t, fontsize=15, color=DARK, fontweight="bold")
        a.set_yticks([])
        a.spines["left"].set_visible(False)
        clean(a, grid=None)
    axs[0].text(0.5, 75.2 * 1.13, "오히려 증가", ha="center", fontsize=12.5, color=ACC)
    fig.tight_layout(w_pad=2.5)
    src(fig, "원문 Figure 2 (left) 기반 재구성 — GPT-2 medium, N=1024, A100")
    save(fig, "p_flash.png")


# ------------------------------------------------------------------ GLU variants Table 1
def fig_glu():
    """Shazeer 2020 Table 1: held-out log-perplexity, 524K step (T5 base, C4)."""
    rows = [("ReLU (원형)", 1.677), ("GELU", 1.679), ("Swish", 1.683), ("GLU", 1.663), ("Bilinear", 1.648),
            ("ReGLU", 1.645), ("GEGLU", 1.633), ("SwiGLU", 1.636)]
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    for i, (n, v) in enumerate(rows):
        c = GRAY if i == 0 else (OFF if i < 3 else (TEAL if n in ("GEGLU", "SwiGLU") else MID))
        ax.barh(i, v - 1.62, left=1.62, color=c, height=0.62)
        ax.text(v + 0.0012, i, f"{v:.3f}", va="center", fontsize=13, color=DARK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(1.62, 1.695)
    ax.set_xticks([1.62, 1.64, 1.66, 1.68])
    ax.set_xlabel("held-out log-perplexity (낮을수록 좋음)")
    clean(ax, grid="x")
    src(fig, "원문 Table 1 기반 재구성 (524K step)")
    save(fig, "p_glu.png")


# ------------------------------------------------------------------ RoPE 회전
def fig_rope():
    """Su et al. 2021 Eq. 12–16 / Figure 1의 아이디어: 위치 m만큼 회전 → 내적은 (m−n)θ에만 의존."""
    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    ax.set_aspect("equal")
    ax.set_xlim(-0.35, 1.55)
    ax.set_ylim(-0.25, 1.35)
    ax.axis("off")
    ax.plot([-0.2, 1.4], [0, 0], color=LINE, lw=1)
    ax.plot([0, 0], [-0.2, 1.25], color=LINE, lw=1)
    base = np.deg2rad(8)
    th = np.deg2rad(16)
    m, n = 4, 1
    for ang, col, lab in [(base + n * th, TEAL, "k_n = R(nθ)·k"), (base + m * th, ACC, "q_m = R(mθ)·q")]:
        x, y = 1.15 * np.cos(ang), 1.15 * np.sin(ang)
        ax.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>", mutation_scale=18, color=col, lw=2.6))
        ax.text(x * 1.05 + (0.02 if col == TEAL else -0.05), y * 1.06, lab, color=col, fontsize=14,
                fontweight="bold", ha="left" if col == TEAL else "center")
    x0, y0 = 1.15 * np.cos(base), 1.15 * np.sin(base)
    ax.add_patch(FancyArrowPatch((0, 0), (x0, y0), arrowstyle="-|>", mutation_scale=14, color=GRAY, lw=1.4,
                                 ls="--"))
    ax.text(x0 + 0.03, y0 - 0.06, "회전 전", color=GRAY, fontsize=12.5)
    ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=np.rad2deg(base + n * th), theta2=np.rad2deg(base + m * th),
                     color=DARK, lw=1.8))
    mid = base + (m + n) / 2 * th
    ax.text(0.5 * np.cos(mid) + 0.04, 0.5 * np.sin(mid) + 0.02, "(m - n)θ", fontsize=14.5, color=DARK,
            fontweight="bold")
    ax.text(-0.3, -0.2, "원문 Eq. 12–16 기반 재구성 (2차원 한 쌍)", fontsize=11.5, color=GRAY)
    save(fig, "p_rope.png")


# ------------------------------------------------------------------ label smoothing 목표
def fig_ls():
    """Szegedy 2016 §7: q' = (1−ε)δ + ε/K. |V|=5, ε=0.1 → (0.92, 0.02, ...)."""
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    x = np.arange(5)
    hard = [1, 0, 0, 0, 0]
    soft = [0.92, 0.02, 0.02, 0.02, 0.02]
    p = [0.7, 0.1, 0.1, 0.05, 0.05]
    w = 0.26
    ax.bar(x - w, hard, w, color=OFF, label="one-hot 정답")
    ax.bar(x, soft, w, color=TEAL, label="smoothed 정답 (ε = 0.1)")
    ax.bar(x + w, p, w, color=ACC_MID, label="모델 예측 p")
    ax.text(0, 0.92 + 0.03, "0.92", ha="center", fontsize=13, color=TEAL, fontweight="bold")
    ax.text(1, 0.02 + 0.03, "0.02", ha="center", fontsize=12.5, color=TEAL, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(["정답", "후보 2", "후보 3", "후보 4", "후보 5"])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("확률")
    ax.legend(frameon=False, fontsize=12.5, loc="upper right")
    clean(ax)
    src(fig, "Szegedy et al. (2016) §7 식으로 계산한 예 (|V| = 5)")
    save(fig, "p_label_smoothing.png")


if __name__ == "__main__":
    for f in (fig_table2, fig_table3, fig_param_gap, fig_xiong, fig_gqa, fig_flash, fig_glu, fig_rope, fig_ls):
        f()
        print("ok", f.__name__)
