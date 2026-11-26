"""Week 5 논문 기반 그림 -> build/assets/week5/paper_*.png (독립 실행: python build/paper_figs_w5.py).

원문 그림은 쓰지 않고 matplotlib 도식으로 새로 그린다. 수치는 build/research/papers/week5.md 에
출처와 함께 적힌 값만 쓴다. (기존 그림은 week5_assets.py — 이 스크립트는 그것들을 건드리지 않는다.)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")
from deckkit import mpl_setup, PALETTE_HEX as P  # noqa: E402

import numpy as np  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager  # noqa: E402
font_manager.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf")
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = os.path.join(HERE, "assets", "week5")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
MINT2, BG, MID, OFF, ACC_MID = (P.get(k) for k in ("MINT2", "BG", "MID", "OFF", "ACC_MID"))
ACC_BG = P.get("ACC_BG")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def rbox(ax, x, y, w, h, text="", fc=MINT, ec=None, fs=15, color=DARK, bold=False, lw=1.2, r=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec or fc, lw=lw))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal")


def arr(ax, x1, y1, x2, y2, color=TEAL2, lw=2.0, ms=16, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def note(fig, text, y=-0.03):
    fig.text(0.5, y, text, ha="center", va="top", fontsize=13, color=GRAY)


# 1. Bahdanau Fig. 1 재구성 ---------------------------------------------------
def fig_bahdanau_arch():
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    xs = [1.4, 3.0, 4.6, 6.2]
    alphas = [0.10, 0.20, 0.55, 0.15]
    labels = ["1", "2", "3", "T"]
    for x, lab in zip(xs, labels):
        rbox(ax, x - 0.45, 0.2, 0.9, 0.6, f"$x_{{{lab}}}$", fc="white", ec=LINE, fs=17)
        rbox(ax, x - 0.5, 1.15, 1.0, 0.6, f"$\\overrightarrow{{h}}_{{{lab}}}$", fc=MINT, fs=17)
        rbox(ax, x - 0.5, 2.0, 1.0, 0.6, f"$\\overleftarrow{{h}}_{{{lab}}}$", fc=MINT2, fs=17)
        arr(ax, x, 0.82, x, 1.13, color=MID)
    for a, b in zip(xs[:-1], xs[1:]):
        arr(ax, a + 0.52, 1.45, b - 0.52, 1.45, color=TEAL2)
        arr(ax, b - 0.52, 2.3, a + 0.52, 2.3, color=TEAL2)
    ax.text(0.1, 1.45, "정방향", fontsize=14, color=GRAY, va="center")
    ax.text(0.1, 2.3, "역방향", fontsize=14, color=GRAY, va="center")
    # annotation brace
    ax.text(7.0, 1.87, "annotation\n$h_j = [\\overrightarrow{h}_j ; \\overleftarrow{h}_j]$", fontsize=15,
            color=DARK, va="center")
    # sum node
    sx, sy = 3.8, 4.15
    ax.add_patch(plt.Circle((sx, sy), 0.32, fc="white", ec=ACC, lw=2.2))
    ax.text(sx, sy, "+", fontsize=22, ha="center", va="center", color=ACC, fontweight="bold")
    for x, a, lab in zip(xs, alphas, labels):
        ax.plot([x, sx], [2.62, sy - 0.32], color=ACC, lw=1 + 9 * a, alpha=0.85, solid_capstyle="round")
        ax.text(x + (sx - x) * 0.2, 2.62 + (sy - 0.32 - 2.62) * 0.2,
                f"$\\alpha_{{t,{lab}}}$", fontsize=15, color=ACC, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=1.5))
    ax.text(sx + 0.45, sy + 0.05, "$c_t$", fontsize=18, color=ACC, va="center")
    # decoder states
    rbox(ax, 1.3, 5.3, 1.3, 0.7, "$s_{t-1}$", fc=MINT, fs=18)
    rbox(ax, 4.3, 5.3, 1.3, 0.7, "$s_t$", fc=TEAL, fs=18, color="white")
    arr(ax, 2.62, 5.65, 4.28, 5.65, color=TEAL2)
    arr(ax, sx + 0.15, sy + 0.3, 4.75, 5.28, color=ACC)
    arr(ax, 1.95, 5.28, sx - 0.2, sy + 0.25, color=GRAY, lw=1.5)
    ax.text(2.1, 4.65, "점수 $e_{t,j}=a(s_{t-1},h_j)$", fontsize=14, color=GRAY, ha="right")
    rbox(ax, 7.0, 5.3, 1.3, 0.7, "$y_t$", fc="white", ec=LINE, fs=18)
    arr(ax, 5.62, 5.65, 6.98, 5.65, color=TEAL2)
    ax.text(5.0, -0.25, "원문 Fig. 1 기반 재구성 (Bahdanau et al., 2014/ICLR 2015) — 선 굵기 = α (설명용 값)",
            fontsize=13, color=GRAY, ha="center")
    save(fig, "paper_bahdanau_arch.png")


# 2. Bahdanau: Fig. 2 경향(개념도) + Table 1 ---------------------------------
def fig_bahdanau_results():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [1, 1.25]})
    x = np.linspace(0, 1, 50)
    curves = [("RNNsearch-50", 0.80 - 0.02 * x, TEAL, "-"),
              ("RNNsearch-30", 0.74 - 0.18 * x ** 1.5, TEAL2, "--"),
              ("RNNencdec-50", 0.62 - 0.32 * x ** 1.3, ACC, "-"),
              ("RNNencdec-30", 0.56 - 0.40 * x ** 1.1, ACC_MID, "--")]
    for name, y, c, ls in curves:
        a1.plot(x, y, color=c, lw=3.2, ls=ls, label=name)
    a1.set_xticks([0.05, 0.95], ["짧은 문장", "긴 문장"], fontsize=14)
    a1.set_yticks([])
    a1.set_ylabel("BLEU (높을수록 좋음)", fontsize=15)
    a1.set_xlabel("원문 문장 길이", fontsize=15)
    a1.legend(fontsize=13, frameon=False, loc="lower left")
    a1.set_title("(a) 길이별 BLEU — 원문 Fig. 2의 경향만", fontsize=16, fontweight="bold", color=DARK, pad=10)
    a1.text(0.5, 0.98, "개념도: 수치 아님", transform=a1.transAxes, fontsize=13, color=GRAY, ha="center",
            va="top")
    a1.set_ylim(0.05, 0.9)

    rows = ["RNNencdec-30", "RNNsearch-30", "RNNencdec-50", "RNNsearch-50", "RNNsearch-50★", "Moses (SMT)"]
    allv = [13.93, 21.50, 17.82, 26.75, 28.45, 33.30]
    nounk = [24.19, 31.44, 26.71, 34.16, 36.15, 35.63]
    y = np.arange(len(rows))[::-1]
    h = 0.38
    cols_all = [MID, TEAL, MID, TEAL, TEAL, GRAY]
    a2.barh(y + h / 2, allv, h, color=cols_all, label="All (전체 문장)")
    a2.barh(y - h / 2, nounk, h, color=[MINT2] * 5 + [OFF], edgecolor=[TEAL] * 5 + [GRAY], lw=1.2,
            label="No UNK (모르는 단어 없는 문장)")
    for yy, v in zip(y, allv):
        a2.text(v + 0.4, yy + h / 2, f"{v:.2f}", va="center", fontsize=13, color=DARK)
    for yy, v in zip(y, nounk):
        a2.text(v + 0.4, yy - h / 2, f"{v:.2f}", va="center", fontsize=13, color=GRAY)
    a2.axvline(33.30, color=ACC, lw=1.6, ls=":")
    a2.set_yticks(y, rows, fontsize=14)
    a2.set_xlim(0, 41)
    a2.set_xlabel("BLEU (WMT'14 영→불 test)", fontsize=15)
    a2.tick_params(axis="x", labelsize=13)
    a2.legend(fontsize=12, frameon=False, loc="lower right", bbox_to_anchor=(1.0, 0.98), ncol=2)
    a2.set_title("(b) 원문 Table 1", fontsize=16, fontweight="bold", color=DARK, pad=32)
    fig.tight_layout(w_pad=3)
    note(fig, "★ 더 오래 학습한 모델.  점선 = Moses 전체 문장 BLEU 33.30 — 전체 test에서는 RNNsearch가 아직 못 미친다.", y=0.0)
    save(fig, "paper_bahdanau_results.png")


# 3. Luong global vs local ----------------------------------------------------
def fig_luong_global_local():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.0))
    S = 10
    xs = np.linspace(0.8, 9.2, S)
    for k, ax in enumerate(axes):
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.9, 5.2)
        ax.axis("off")
        pt = 6
        if k == 1:
            D = 2
            lo, hi = pt - D, pt + D
            ax.add_patch(FancyBboxPatch((xs[lo] - 0.5, 0.15), xs[hi] - xs[lo] + 1.0, 1.2,
                                        boxstyle="round,pad=0,rounding_size=0.1", fc=ACC_BG, ec=ACC, lw=1.5,
                                        ls="--"))
            g = np.exp(-((np.arange(S) - pt) ** 2) / (2 * (D / 2) ** 2))
            xx = np.linspace(xs[lo], xs[hi], 100)
            ax.plot(xx, 1.7 + 0.9 * np.exp(-((xx - xs[pt]) ** 2) / (2 * ((xs[1] - xs[0]) * D / 2) ** 2)),
                    color=ACC, lw=2)
            ax.text(xs[pt], 0.0, "$p_t$", fontsize=17, color=ACC, ha="center", va="top")
            ax.text(xs[lo] - 0.5, -0.45, "$[p_t - D,\\ p_t + D]$ 창만", fontsize=14, color=ACC, va="top")
            ws = np.where((np.arange(S) >= lo) & (np.arange(S) <= hi), g, 0)
        else:
            ws = np.array([.03, .04, .05, .08, .12, .2, .25, .12, .07, .04])
        ws = ws / ws.sum()
        for i, x in enumerate(xs):
            on = ws[i] > 0
            rbox(ax, x - 0.36, 0.35, 0.72, 0.8, f"$\\bar h_{{{i+1}}}$", fc=MINT if on else OFF, fs=14,
                 color=DARK if on else GRAY)
            if on:
                ax.plot([x, 5.0], [1.17, 3.85], color=TEAL, lw=0.8 + 10 * ws[i], alpha=0.8)
        rbox(ax, 4.4, 3.85, 1.2, 0.75, "$h_t$", fc=TEAL, fs=18, color="white")
        ax.text(5.9, 4.22, "디코더 현재 상태", fontsize=14, color=GRAY, va="center")
        ax.set_title(["(a) Global: 모든 원문 위치", "(b) Local-p: 위치 $p_t$를 예측하고 창 안만 (Gaussian 가중)"][k],
                     fontsize=16, fontweight="bold", color=DARK)
    note(fig, "원문 Fig. 2 · Fig. 3 기반 재구성 (Luong et al., EMNLP 2015) — 논문 설정은 D = 10, σ = D/2. 그림은 D = 2.", y=0.02)
    save(fig, "paper_luong_global_local.png")


# 4. Luong Table 4 ------------------------------------------------------------
def fig_luong_table4():
    rows = ["global (location)", "global (dot)", "global (general)", "local-m (dot)", "local-m (general)",
            "local-p (dot)", "local-p (general)"]
    pre = [18.1, 18.6, 17.3, None, 18.6, 18.0, 19.0]
    post = [19.3, 20.5, 19.1, None, 20.4, 19.6, 20.9]
    fig, ax = plt.subplots(figsize=(10, 5.6))
    y = np.arange(len(rows))[::-1]
    h = 0.38
    for yy, a, b, name in zip(y, pre, post, rows):
        if a is None:
            ax.text(15.2, yy, "학습 실패 (perplexity > 7)", fontsize=14, color=ACC, va="center")
            continue
        best = name == "local-p (general)" or name == "global (dot)"
        ax.barh(yy + h / 2, a, h, color=TEAL if best else MID)
        ax.barh(yy - h / 2, b, h, color=MINT2, edgecolor=TEAL, lw=1.2)
        ax.text(a + 0.08, yy + h / 2, f"{a}", va="center", fontsize=13)
        ax.text(b + 0.08, yy - h / 2, f"{b}", va="center", fontsize=13, color=GRAY)
    ax.set_yticks(y, rows, fontsize=14)
    ax.set_xlim(15, 22.2)
    ax.set_xlabel("BLEU (WMT'14 영→독 newstest2014) — 가로축은 15부터", fontsize=14)
    ax.tick_params(axis="x", labelsize=13)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=MID, label="unk 대체 전 (진한 색 = 원문이 꼽은 최선)"),
                       Patch(fc=MINT2, ec=TEAL, label="unk 대체 후")],
              fontsize=13, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.13), ncol=2)
    ax.set_title("원문 Table 4: 정렬 방식 × 점수 함수", fontsize=16, fontweight="bold", color=DARK)
    save(fig, "paper_luong_table4.png")


# 5. Vaswani Fig. 2 재구성 ----------------------------------------------------
def fig_vaswani_fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6.6), gridspec_kw={"width_ratios": [1, 1.15]})
    for ax in (a1, a2):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 7.4)
        ax.axis("off")
    # left: scaled dot-product
    steps = [("MatMul", MINT), ("Scale  ÷ $\\sqrt{d_k}$", MINT), ("Mask (선택)", OFF), ("SoftMax", ACC_BG), ("MatMul", MINT)]
    ys = [1.4, 2.5, 3.6, 4.7, 5.8]
    for (t, c), y in zip(steps, ys):
        rbox(a1, 1.4, y, 2.6, 0.7, t, fc=c, fs=16, bold=True, ec=ACC if t == "SoftMax" else None)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        arr(a1, 2.7, y0 + 0.72, 2.7, y1 - 0.02)
    a1.text(1.9, 0.6, "Q", fontsize=19, ha="center", fontweight="bold", color=DARK)
    a1.text(3.5, 0.6, "K", fontsize=19, ha="center", fontweight="bold", color=DARK)
    a1.text(5.5, 0.6, "V", fontsize=19, ha="center", fontweight="bold", color=DARK)
    arr(a1, 1.9, 0.95, 2.2, 1.38)
    arr(a1, 3.5, 0.95, 3.2, 1.38)
    a1.plot([5.5, 5.5], [0.95, 6.15], color=TEAL2, lw=2)
    arr(a1, 5.5, 6.15, 4.02, 6.15)
    arr(a1, 2.7, 6.52, 2.7, 7.1)
    a1.text(4.15, 3.95, "−∞ (§3.2.3)", fontsize=13, color=GRAY, va="center")
    a1.set_title("(a) Scaled Dot-Product Attention", fontsize=16, fontweight="bold", color=DARK)
    # right: multi-head
    for k in range(3):
        off = 0.12 * (2 - k)
        rbox(a2, 0.9 + off, 1.4 + off, 4.2, 0.7, "", fc=[MINT2, MINT, MINT][k], ec=LINE)
        rbox(a2, 0.9 + off, 3.0 + off, 4.2, 0.9, "", fc=[OFF, ACC_BG, ACC_BG][k], ec=LINE)
    a2.text(3.0, 1.75, "Linear × 3  (head마다 $W_i^Q, W_i^K, W_i^V$)", fontsize=14, ha="center", va="center")
    a2.text(3.0, 3.45, "Scaled Dot-Product Attention", fontsize=15, ha="center", va="center", fontweight="bold")
    a2.text(5.35, 3.55, "h 개\n병렬", fontsize=14, color=ACC, va="center", fontweight="bold")
    rbox(a2, 1.6, 4.65, 2.8, 0.7, "Concat", fc=MINT, fs=16, bold=True)
    rbox(a2, 1.6, 5.85, 2.8, 0.7, "Linear  ($W^O$)", fc=TEAL, fs=16, bold=True, color="white")
    arr(a2, 3.0, 2.25, 3.0, 2.98)
    arr(a2, 3.0, 4.05, 3.0, 4.63)
    arr(a2, 3.0, 5.37, 3.0, 5.83)
    arr(a2, 3.0, 6.57, 3.0, 7.1)
    for x, t in zip([1.6, 3.0, 4.4], ["V", "K", "Q"]):
        a2.text(x, 0.6, t, fontsize=19, ha="center", fontweight="bold", color=DARK)
        arr(a2, x, 0.95, x, 1.38)
    a2.text(4.55, 6.2, "← v1 식에는 없음\n   (NIPS판 · arXiv v2+)", fontsize=12.5, color=ACC, va="center")
    a2.set_title("(b) Multi-Head Attention", fontsize=16, fontweight="bold", color=DARK)
    note(fig, "원문 Fig. 2 기반 재구성 (Vaswani et al., NIPS 2017)", y=0.02)
    save(fig, "paper_vaswani_fig2.png")


# 6. Table 3 (A): head 수 -----------------------------------------------------
def fig_table3a():
    hs = [1, 4, 8, 16, 32]
    bleu = [24.9, 25.5, 25.8, 25.8, 25.4]
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    xs = np.arange(len(hs))
    ax.plot(xs, bleu, color=TEAL2, lw=2.5, zorder=1)
    for x, h, b in zip(xs, hs, bleu):
        base = h == 8
        ax.scatter([x], [b], s=230 if base else 160, color=ACC if base else TEAL, zorder=2)
        ax.text(x, b + 0.09, f"{b}", ha="center", fontsize=15, fontweight="bold", color=ACC if base else DARK)
    ax.set_xticks(xs, [f"h = {h}\n$d_k$ = {512 // h}" for h in hs], fontsize=14)
    ax.set_ylim(24.6, 26.15)
    ax.set_yticks([24.75, 25.0, 25.25, 25.5, 25.75, 26.0])
    ax.tick_params(axis="y", labelsize=13)
    ax.set_ylabel("dev BLEU (세로축 24.6부터)", fontsize=14)
    ax.annotate("base (h = 8)", (2, 25.8), (2.35, 25.15), fontsize=14, color=ACC,
                arrowprops=dict(arrowstyle="-|>", color=ACC))
    ax.annotate("head 1개: 최고보다 0.9 낮음", (0, 24.9), (0.25, 24.68), fontsize=13.5, color=GRAY)
    ax.set_title("원문 Table 3 (A) — 계산량을 고정하고 head 수만 바꿈", fontsize=15, fontweight="bold", color=DARK)
    ax.grid(axis="y", color=P.get("GRID"), lw=1)
    save(fig, "paper_table3a.png")


# 7. 최대 경로 길이 (§4 Table 1) ---------------------------------------------
def fig_path_length():
    n = 6
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    xs = np.linspace(0.6, 5.4, n)
    titles = ["Recurrent: 경로 O(n)", "Convolution (k = 3): 층을 쌓아야", "Self-attention: 경로 O(1)"]
    for ax, t in zip(axes, titles):
        ax.set_xlim(0, 6)
        ax.set_ylim(-0.9, 4.2)
        ax.axis("off")
        ax.set_title(t, fontsize=17, fontweight="bold", color=DARK)
    # RNN
    ax = axes[0]
    for i, x in enumerate(xs):
        c = ACC if i in (0, n - 1) else MINT
        ax.add_patch(plt.Circle((x, 1.6), 0.3, fc=c, ec="none"))
        ax.text(x, 0.9, f"$x_{i+1}$", ha="center", fontsize=15, va="top")
        if i < n - 1:
            arr(ax, x + 0.32, 1.6, xs[i + 1] - 0.32, 1.6, color=ACC, lw=2.5)
    ax.text(3.0, 2.6, f"{n - 1}단계를 차례로 거친다", ha="center", fontsize=15, color=ACC)
    # Conv
    ax = axes[1]
    layers = 3
    for l in range(layers + 1):
        for i, x in enumerate(xs):
            on = (l == 0 and i in (0, n - 1))
            ax.add_patch(plt.Circle((x, 0.4 + l * 1.15), 0.22, fc=ACC if on else MINT, ec="none"))
    # receptive path from top node (i=3?) — highlight top node covering all
    top = (xs[2] + xs[3]) / 2
    path_nodes = [[(xs[0], 0.4), (xs[1], 1.55), (xs[2], 2.7)], [(xs[5], 0.4), (xs[4], 1.55), (xs[3], 2.7)]]
    for pn in path_nodes:
        for (x0, y0), (x1, y1) in zip(pn[:-1], pn[1:]):
            ax.plot([x0, x1], [y0, y1], color=ACC, lw=2.5)
    ax.plot([xs[2], top], [2.7, 3.85], color=ACC, lw=2.5)
    ax.plot([xs[3], top], [2.7, 3.85], color=ACC, lw=2.5)
    ax.add_patch(plt.Circle((top, 3.85), 0.22, fc=ACC, ec="none"))
    ax.text(3.0, -0.35, "연속 커널: O(n/k)층 · dilated: O(log$_k$ n)", fontsize=14, color=GRAY, ha="center", va="top")
    # SA
    ax = axes[2]
    for i, x in enumerate(xs):
        for j, x2 in enumerate(xs):
            if i < j:
                hl = (i, j) == (0, n - 1)
                h = 0.25 + 0.42 * (j - i)
                t = np.linspace(0, np.pi, 40)
                ax.plot((x + x2) / 2 + (x2 - x) / 2 * np.cos(t), 1.0 + h * np.sin(t),
                        color=ACC if hl else MID, lw=3 if hl else 1, alpha=1 if hl else 0.7)
    for i, x in enumerate(xs):
        ax.add_patch(plt.Circle((x, 1.0), 0.3, fc=ACC if i in (0, n - 1) else MINT, ec="none"))
        ax.text(x, 0.4, f"$x_{i+1}$", ha="center", fontsize=15, va="top")
    ax.text(3.0, 3.75, "한 층에서 바로 연결 (대신 쌍이 $n^2$개)", ha="center", fontsize=14, color=ACC)
    note(fig, "주황 = 가장 먼 두 위치 $x_1$ ↔ $x_6$ 을 잇는 경로. 원문 §4 Table 1의 '최대 경로 길이'를 그림으로 옮긴 개념도", y=0.02)
    save(fig, "paper_path_length.png")


# 8. Wiegreffe & Pinter Table 2: uniform 기준선 -------------------------------
def fig_wp_uniform():
    ds = ["SST", "AgNews", "IMDb", "Diabetes"]
    learned = [0.831, 0.964, 0.902, 0.775]
    uni = [0.822, 0.960, 0.879, 0.706]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    x = np.arange(len(ds))
    w = 0.36
    ax.bar(x - w / 2, learned, w, color=TEAL, label="학습된 attention")
    ax.bar(x + w / 2, uni, w, color=MINT2, edgecolor=TEAL, lw=1.2, label="균등(uniform) attention으로 고정")
    for xx, a, b in zip(x, learned, uni):
        ax.text(xx - w / 2, a + 0.008, f"{a:.3f}", ha="center", fontsize=13)
        ax.text(xx + w / 2, b + 0.008, f"{b:.3f}", ha="center", fontsize=13, color=GRAY)
    ax.set_xticks(x, ds, fontsize=15)
    ax.set_ylim(0.6, 1.02)
    ax.tick_params(axis="y", labelsize=13)
    ax.set_ylabel("원문 Table 2의 점수 (세로축 0.6부터)", fontsize=13.5)
    ax.legend(fontsize=13, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    ax.set_title("Wiegreffe & Pinter (2019) Table 2 — BiLSTM 분류기", fontsize=15, fontweight="bold", color=DARK)
    save(fig, "paper_wp_uniform.png")


if __name__ == "__main__":
    fig_bahdanau_arch()
    fig_bahdanau_results()
    fig_luong_global_local()
    fig_luong_table4()
    fig_vaswani_fig2()
    fig_table3a()
    fig_path_length()
    fig_wp_uniform()
    print(sorted(f for f in os.listdir(OUT) if f.startswith("paper_")))
