"""Week 1 논문 그림 (독립 실행): python paper_figs_w1.py → build/assets/week1/paper_*.png

논문 원본 이미지는 쓰지 않고, 원문 그림의 구조를 matplotlib 도식으로 새로 그린다.
근거: build/research/papers/week1.md
  - McCulloch & Pitts (1943) Figure 1b–d        → paper_mp_fig1.png
  - Widrow & Hoff (1960) §C, Fig.2–3 (4×4 판)   → paper_adaline_board.png
  - Widrow & Hoff (1960) Fig.1, Fig.3 (뉴런 소자) → paper_adaline_unit.png
  - Widrow & Hoff (1960) Fig.10, p.99–100, 104 → paper_wh_fig10.png
  - Widrow & Hoff (1960) p.99 one-pattern-at-a-time (LMS) vs 전체 평균 → paper_lms_vs_batch.png
  - Cauchy (1847) via Lemaréchal (2012) 식 (1)–(3) → paper_cauchy_step.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")
from deckkit import mpl_setup, PALETTE_HEX as P  # noqa: E402

import numpy as np  # noqa: E402
import logging  # noqa: E402
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

plt = mpl_setup()
from matplotlib import font_manager  # noqa: E402
_bold = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
if os.path.exists(_bold):
    font_manager.fontManager.addfont(_bold)
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]  # 한글 + 기호(₁, ε, Σ) fallback
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

OUT = os.path.join(HERE, "assets", "week1")
T, T2, A, G, D = P["TEAL"], P["TEAL2"], P["ACCENT"], P["GRAY"], P["DARK"]
M, M2, LN = P["MINT"], P.get("MINT2", "#D6E6FA"), P["LINE"]
ACC_BG = P.get("ACC_BG", "#FFF3EA")


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("saved", p)
    return p


def _arrow(ax, p, q, color=G, lw=2.0, style="-|>", ms=16):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 shrinkA=0, shrinkB=0))


# ------------------------------------------------------------------ 1. McCulloch–Pitts Figure 1b–d
def mp_fig1():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.9))
    panels = [("(b) OR", [2, 2], [False, False], r"$N_3(t) \equiv N_1(t-1) \vee N_2(t-1)$", "입력마다 종말 2개"),
              ("(c) AND", [1, 1], [False, False], r"$N_3(t) \equiv N_1(t-1) \cdot N_2(t-1)$", "입력마다 종말 1개"),
              ("(d) AND-NOT", [2, 0], [False, True], r"$N_3(t) \equiv N_1(t-1) \cdot \sim N_2(t-1)$", "$N_2$는 억제 (거부권)")]
    for ax, (title, ends, inhib, eq, sub) in zip(axes, panels):
        ax.set_xlim(0, 10); ax.set_ylim(0.0, 8.6); ax.set_aspect("equal"); ax.axis("off")
        ax.text(5, 8.25, title, ha="center", va="center", fontsize=19, fontweight="bold", color=T)
        # 뉴런 3 (삼각형 머리)
        tri = Polygon([[6.0, 3.2], [6.0, 6.0], [8.2, 4.6]], closed=True, fc=M2, ec=T, lw=2)
        ax.add_patch(tri)
        ax.text(6.75, 4.6, "3", ha="center", va="center", fontsize=17, fontweight="bold", color=D)
        ax.text(7.0, 2.65, "θ = 2", ha="center", va="center", fontsize=15, color=D)
        _arrow(ax, (8.2, 4.6), (9.7, 4.6), color=T, lw=2.4)
        for k, (yy, n, inh) in enumerate(zip([6.6, 2.6], ends, inhib)):
            lab = f"{k + 1}"
            ax.add_patch(Circle((1.2, yy), 0.55, fc="white", ec=G, lw=2))
            ax.text(1.2, yy, lab, ha="center", va="center", fontsize=16, fontweight="bold", color=D)
            ty = 5.25 if k == 0 else 3.95
            ax.plot([1.75, 5.25], [yy, ty], color=G, lw=2)
            if inh:  # 억제: 빈 고리
                ax.add_patch(Circle((5.5, ty), 0.28, fc="white", ec=A, lw=2.6))
                ax.text(3.3, (yy + ty) / 2 - 0.75, "억제", ha="center", va="center", fontsize=14,
                        color=A, fontweight="bold")
            else:
                for j in range(n):  # 흥분 시냅스 종말(●)
                    off = (j - (n - 1) / 2) * 0.55
                    ax.plot([5.25, 5.75], [ty, ty + off], color=G, lw=1.6)
                    ax.add_patch(Circle((5.82, ty + off), 0.17, fc=T, ec=T))
        ax.text(5, 1.45, eq, ha="center", va="center", fontsize=15, color=D)
        ax.text(5, 0.5, sub, ha="center", va="center", fontsize=14, color=G)
    fig.text(0.5, 0.02, "McCulloch & Pitts (1943) Figure 1 기반 재구성 · ● 흥분 시냅스 종말, ○ 억제 시냅스 · 출력은 한 시냅스 지연 뒤",
             ha="center", fontsize=13, color=G)
    fig.tight_layout()
    return _save(fig, "paper_mp_fig1.png")


# ------------------------------------------------------------------ 2. ADALINE 4×4 스위치 판 = 텐서
def adaline_board():
    pat = np.array([[1, 1, 1, 1], [-1, 1, -1, -1], [-1, 1, -1, -1], [-1, 1, -1, -1]])  # 설명용 'T'
    fig, ax = plt.subplots(figsize=(12.8, 4.3))
    ax.set_xlim(0, 25.8); ax.set_ylim(0, 8.6); ax.set_aspect("equal"); ax.axis("off")
    c = 1.25
    x0, y0 = 0.6, 7.3
    for r in range(4):
        for k in range(4):
            v = pat[r, k]
            ax.add_patch(Rectangle((x0 + k * c, y0 - (r + 1) * c), c, c, fc=T if v > 0 else "white", ec="white" if v > 0 else T, lw=1.6))
            ax.text(x0 + (k + .5) * c, y0 - (r + .5) * c, "+1" if v > 0 else "−1", ha="center", va="center",
                    fontsize=13, color="white" if v > 0 else G, fontweight="bold")
    ax.text(x0 + 2 * c, y0 + 0.65, "토글 스위치 4×4 판", ha="center", fontsize=16, fontweight="bold", color=D)
    ax.text(x0 + 2 * c, y0 - 4 * c - 0.65, "shape (4, 4)", ha="center", fontsize=16, color=T, fontweight="bold")
    # reshape 화살표
    _arrow(ax, (6.3, 4.8), (8.3, 4.8), color=G, lw=2.4)
    ax.text(7.3, 5.45, "reshape", ha="center", fontsize=14, color=G)
    # 16칸 띠 (2줄로 8칸씩이 아니라 한 줄)
    s = 0.88
    flat = pat.reshape(-1)
    sx, sy = 8.6, 5.25
    for i, v in enumerate(flat):
        ax.add_patch(Rectangle((sx + i * s, sy - s), s, s, fc=T if v > 0 else "white", ec="white" if v > 0 else T, lw=1.3))
    ax.text(sx + 8 * s, sy + 0.4, "입력 s  shape (16,)", ha="center", fontsize=15, color=T, fontweight="bold")
    # 가중치 띠
    wy = 3.35
    for i in range(16):
        ax.add_patch(Rectangle((sx + i * s, wy - s), s, s, fc=M2, ec=G, lw=1.0))
        ax.text(sx + (i + .5) * s, wy - s / 2, "a", ha="center", va="center", fontsize=11, color=D)
    ax.text(sx + 8 * s, wy - s - 0.6, r"이득(가중치) $a_1 \ldots a_{16}$   shape (16,)", ha="center", fontsize=15, color=D)
    ax.add_patch(Circle((sx - 0.5, (sy + wy) / 2 - 0.45), 0.13, fc=D, ec=D))
    # 결과
    _arrow(ax, (sx + 16 * s + 0.3, 3.9), (sx + 16 * s + 1.4, 3.9), color=G, lw=2.4)
    bx = sx + 16 * s + 1.6
    ax.add_patch(FancyBboxPatch((bx, 2.5), 0.9 + 0.0, 2.8, boxstyle="round,pad=0.12", fc=ACC_BG, ec=A, lw=1.8))
    ax.text(bx + 0.45, 4.6, "Σ", ha="center", va="center", fontsize=22, color=A, fontweight="bold")
    ax.text(bx + 0.45, 3.35, r"$+a_0$", ha="center", va="center", fontsize=13, color=A)
    ax.text(12.0, 0.45, r"내적 $a \cdot s + a_0$   →   손잡이(파라미터) 16 + 1 = 17개", ha="center", fontsize=17,
            color=D, fontweight="bold")
    ax.text(25.7, 8.2, "Widrow & Hoff (1960) §C 기반 재구성\n(패턴 모양은 설명용)", ha="right", va="center",
            fontsize=11.5, color=G)
    return _save(fig, "paper_adaline_board.png")


# ------------------------------------------------------------------ 3. ADALINE 뉴런 소자 (Fig.1 + Fig.3)
def adaline_unit():
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 23); ax.set_ylim(-1.0, 11.2); ax.set_aspect("equal"); ax.axis("off")
    ins = [("+1", 9.4), (r"$s_1$", 7.7), (r"$s_2$", 6.0), ("⋮", 4.6), (r"$s_n$", 3.2)]
    sx, kx, cx = 1.2, 5.0, 9.6
    for lab, y in ins:
        if lab == "⋮":
            ax.text(sx, y, "⋮", ha="center", va="center", fontsize=22, color=G)
            continue
        ax.add_patch(Circle((sx, y), 0.6, fc="white", ec=G, lw=2))
        ax.text(sx, y, lab, ha="center", va="center", fontsize=16, color=D, fontweight="bold")
        ax.plot([sx + 0.6, kx - 0.7], [y, y], color=G, lw=1.8)
        idx = {"+1": r"$a_0$", r"$s_1$": r"$a_1$", r"$s_2$": r"$a_2$", r"$s_n$": r"$a_n$"}[lab]
        ax.add_patch(FancyBboxPatch((kx - 0.7, y - 0.5), 1.4, 1.0, boxstyle="round,pad=0.05", fc=M2, ec=T, lw=1.8))
        ax.text(kx, y, idx, ha="center", va="center", fontsize=16, color=D, fontweight="bold")
        ax.plot([kx + 0.7, cx - 0.85], [y, 6.3 + (y - 6.3) * 0.15], color=G, lw=1.8)
    ax.text(sx, 10.65, "입력 ±1", ha="center", fontsize=14, color=G)
    ax.text(kx, 10.65, "이득 a (±)", ha="center", fontsize=14, color=G)
    ax.add_patch(Circle((cx, 6.3), 0.85, fc=M2, ec=T, lw=2.2))
    ax.text(cx, 6.3, "Σ", ha="center", va="center", fontsize=24, color=T, fontweight="bold")
    # 양자화기
    qx = 14.0
    ax.plot([cx + 0.85, qx - 1.0], [6.3, 6.3], color=G, lw=2.2)
    ax.add_patch(FancyBboxPatch((qx - 1.0, 5.3), 2.0, 2.0, boxstyle="round,pad=0.05", fc="white", ec=T, lw=2))
    ax.plot([qx - 0.7, qx, qx, qx + 0.7], [5.75, 5.75, 6.85, 6.85], color=T, lw=2.4)
    ax.text(qx, 7.75, "양자화기", ha="center", fontsize=14, color=G)
    _arrow(ax, (qx + 1.0, 6.3), (17.4, 6.3), color=T, lw=2.4)
    ax.text(18.9, 6.3, "출력 ±1", ha="center", va="center", fontsize=16, color=D, fontweight="bold")
    ax.text(18.9, 5.45, "(분류)", ha="center", va="center", fontsize=13, color=G)
    # 오차: 양자화 전에서 딴다
    tap = 11.6
    ax.add_patch(Circle((tap, 6.3), 0.13, fc=A, ec=A))
    ax.plot([tap, tap], [6.3, 2.0], color=A, lw=2.4)
    ax.add_patch(Circle((tap, 1.4), 0.6, fc=ACC_BG, ec=A, lw=2.2))
    ax.text(tap, 1.4, "−", ha="center", va="center", fontsize=22, color=A, fontweight="bold")
    ax.text(tap + 0.55, 4.6, "선형 출력 (양자화 전)", ha="left", va="center", fontsize=13.5, color=A)
    ax.plot([15.6, tap + 0.6], [1.4, 1.4], color=A, lw=2.0)
    ax.text(17.8, 1.4, "원하는 출력 d\n(기준 스위치)", ha="center", va="center", fontsize=14, color=D)
    _arrow(ax, (tap - 0.6, 1.4), (7.9, 1.4), color=A, lw=2.4)
    ax.text(5.6, 1.4, "오차 ε = d − Σ", ha="center", va="center", fontsize=16, color=A, fontweight="bold")
    ax.text(5.6, 0.45, "→ 계기판 · 이득 조정", ha="center", va="center", fontsize=13.5, color=G)
    ax.text(11.5, -0.75, "Widrow & Hoff (1960) Fig.1·Fig.3 기반 재구성 — 오차는 양자화 '전' 선형 출력에서 잰다",
            ha="center", fontsize=12.5, color=G)
    return _save(fig, "paper_adaline_unit.png")


# ------------------------------------------------------------------ 4. W&H Fig.10: 10개로 학습 → 100개로 시험
def wh_fig10():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    labs = ["10개\n#1", "10개\n#2", "10개\n#3", "10개\n#4", "100개 전부\n(best)"]
    errs = [25, 19, 20, 28, 12]
    cols = [T2, T2, T2, T2, A]
    b = a1.bar(range(5), errs, color=cols, width=0.62)
    for i, e in enumerate(errs):
        a1.text(i, e + 0.8, str(e), ha="center", fontsize=16, fontweight="bold", color=D)
    a1.set_xticks(range(5)); a1.set_xticklabels(labs, fontsize=13)
    a1.set_ylabel("오류 수 (시험 패턴 100개 중)", fontsize=14)
    a1.set_ylim(0, 33); a1.tick_params(axis="y", labelsize=13)
    a1.set_title("몇 개로 학습했나 → 100개 시험 오류", fontsize=16, color=T, fontweight="bold")
    mis = [108, 58, 67, 133]
    a2.bar(range(4), mis, color=T2, width=0.6)
    for i, m in enumerate(mis):
        a2.text(i, m + 3, f"{m}%", ha="center", fontsize=15, fontweight="bold", color=D)
    a2.axhline(100, color=A, lw=2.2, ls="--")
    a2.text(3.45, 103, "이론 M = (n+1)/N = 100%", ha="right", va="bottom", fontsize=13.5, color=A)
    a2.axhline(91.5, color=G, lw=1.6, ls=":")
    a2.text(1.0, 88, "평균 91.5%", ha="center", va="top", fontsize=13.5, color=G)
    a2.set_xticks(range(4)); a2.set_xticklabels(["#1", "#2", "#3", "#4"], fontsize=13)
    a2.set_ylim(0, 150); a2.set_ylabel("오조정 M", fontsize=14); a2.tick_params(axis="y", labelsize=13)
    a2.set_title("10개로 학습한 네 번의 오조정", fontsize=16, color=T, fontweight="bold")
    fig.text(0.5, -0.03, "Widrow & Hoff (1960) Fig.10, p.99–100 기반 재구성 · 3×3 패턴 X·T·C·J + 10% 잡음 · 시험 100개에는 학습한 10개가 포함됨",
             ha="center", fontsize=12.5, color=G)
    fig.tight_layout()
    return _save(fig, "paper_wh_fig10.png")


# ------------------------------------------------------------------ 5. LMS(한 패턴씩) vs 전체 평균 한 걸음
def lms_vs_batch():
    x = np.array([1., 2., 3., 4.]); y = np.array([3., 5., 7., 9.])
    eta = 0.05
    # 전체 평균(full-batch) 경사하강 3걸음
    bp = [(0.0, 0.0)]
    w = b = 0.0
    for _ in range(3):
        e = w * x + b - y
        w, b = w - eta * np.mean(2 * e * x), b - eta * np.mean(2 * e)
        bp.append((w, b))
    # LMS: 한 패턴씩 (W ← W + 2μεX, μ = η/2)
    lp = [(0.0, 0.0)]
    w = b = 0.0
    for xi, yi in zip(x, y):
        eps = yi - (w * xi + b)
        w, b = w + eta * eps * xi, b + eta * eps
        lp.append((w, b))
    mse = lambda w, b: np.mean((w * x + b - y) ** 2)
    print("batch", [tuple(round(v, 4) for v in p) for p in bp], "LMS", [tuple(round(v, 3) for v in p) for p in lp],
          "LMS MSE", round(mse(*lp[-1]), 3))
    W, B = np.meshgrid(np.linspace(-0.3, 2.6, 300), np.linspace(-0.4, 1.6, 300))
    Z = ((W[..., None] * x + B[..., None] - y) ** 2).mean(-1)
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    ax.contour(W, B, Z, levels=[0.05, 0.3, 1, 3, 8, 16, 26, 38], colors=LN, linewidths=1.2)
    ax.plot(*zip(*bp), "-o", color=T, lw=2.6, ms=8, label="전체 평균: 1 epoch = 한 걸음")
    ax.plot(*zip(*lp), "-s", color=A, lw=2.2, ms=7, label="LMS(한 패턴씩): 1 epoch = 네 걸음")
    ax.plot([2], [1], marker="*", ms=20, color=D, ls="none")
    ax.text(2.06, 1.06, "정답 (2, 1)", fontsize=14, color=D)
    ax.annotate("1 epoch 뒤\n(1.75, 0.60)\nL = 1.13", bp[1], xytext=(1.05, -0.3), fontsize=13, color=T,
                arrowprops=dict(arrowstyle="-|>", color=T, lw=1.4))
    ax.annotate("1 epoch 뒤\n(1.94, 0.77)\nL = 0.14", lp[-1], xytext=(2.05, 0.15), fontsize=13, color=A,
                arrowprops=dict(arrowstyle="-|>", color=A, lw=1.4))
    ax.set_xlabel("w", fontsize=15); ax.set_ylabel("b", fontsize=15)
    ax.tick_params(labelsize=13)
    ax.legend(fontsize=12.5, loc="upper left", frameon=False)
    ax.set_xlim(-0.3, 2.6); ax.set_ylim(-0.4, 1.6)
    return _save(fig, "paper_lms_vs_batch.png")


# ------------------------------------------------------------------ 6. Cauchy 한 걸음
def cauchy_step():
    X, Y = np.meshgrid(np.linspace(-0.8, 4.2, 300), np.linspace(-2.4, 1.0, 300))
    F = (X - 3) ** 2 + (Y + 1) ** 2
    fig, ax = plt.subplots(figsize=(6.4, 4.9))
    ax.contour(X, Y, F, levels=[0.5, 1, 2.5, 5, 10, 15], colors=LN, linewidths=1.2)
    ax.contour(X, Y, F, levels=[2.5, 10], colors=[A, T], linewidths=1.6, linestyles="--")
    _arrow(ax, (0, 0), (1.5, -0.5), color=A, lw=2.6, ms=20)
    ax.plot([0], [0], "o", color=T, ms=10)
    ax.plot([1.5], [-0.5], "o", color=A, ms=10)
    ax.plot([3], [-1], marker="*", ms=18, color=D)
    ax.text(0.4, 0.06, "시작 (0, 0)  f = 10", fontsize=14, color=T)
    ax.text(1.55, -0.32, "(1.5, −0.5)  f = 2.5", fontsize=14, color=A)
    ax.text(3.08, -1.25, "최소 (3, −1)", fontsize=14, color=D)
    ax.set_xlabel("x", fontsize=15); ax.set_ylabel("y", fontsize=15); ax.tick_params(labelsize=13)
    ax.set_aspect("equal")
    ax.set_title(r"$f(x, y) = (x-3)^2 + (y+1)^2$", fontsize=16, color=D)
    return _save(fig, "paper_cauchy_step.png")


def make_all():
    mp_fig1(); adaline_board(); adaline_unit(); wh_fig10(); lms_vs_batch(); cauchy_step()


if __name__ == "__main__":
    make_all()
